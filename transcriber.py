import threading
import queue
import numpy as np
import torch
import os
from datetime import datetime
from abc import ABC, abstractmethod
from collections import deque
import re

def print_supported_gpu_devices():
    """
    Checks for CUDA availability and prints the detected GPU devices.
    """
    if torch.cuda.is_available():
        print(f"CUDA is available. Number of GPUs: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("CUDA is not available. Running on CPU.")

class AbstractTranscriber(ABC, threading.Thread):
    """
    Abstract base class for transcriber implementations.
    """
    def __init__(self, transcription_queue, word_display_manager, model_loaded_event, 
                 model_name="tiny.en", sample_rate=44100, device="cpu",
                 interval_seconds=0.5, overlap_seconds=0.1,
                 transcription_history_size=50, cleanup_strategy="none"):
        super().__init__()
        self.transcription_queue = transcription_queue
        self.word_display_manager = word_display_manager # Direct reference to the display manager
        self.model_loaded_event = model_loaded_event
        self.model_name = model_name
        self.sample_rate = sample_rate
        self.device = device
        self.interval_seconds = interval_seconds
        self.overlap_seconds = overlap_seconds
        self.transcription_history_size = transcription_history_size
        self.cleanup_strategy = cleanup_strategy
        self.transcription_history = deque(maxlen=transcription_history_size)
        self._running = False
        self.model = None
        self.audio_buffer = bytearray()

        # --- Setup for Logging ---
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file_path = os.path.join(log_dir, f"transcription_{timestamp}.log")

    @abstractmethod
    def _load_model(self):
        pass

    @abstractmethod
    def _transcribe_audio(self, audio_np):
        pass

    def run(self):
        """
        The main loop of the transcriber thread.
        """
        # Calculate buffer sizes in bytes using instance attributes from config
        interval_buffer_size = int(self.sample_rate * self.interval_seconds) * 2 # 2 bytes per int16 sample
        overlap_buffer_size = int(self.sample_rate * self.overlap_seconds) * 2 # 2 bytes per int16 sample

        self._load_model()
        print(f"Whisper model loaded on {self.device}. Performing warm-up inference...")
        # Perform a warm-up inference with a silent audio chunk
        warmup_audio_duration = 1.0 # seconds
        silent_audio_np = np.zeros(int(self.sample_rate * warmup_audio_duration), dtype=np.float32)
        try:
            self._transcribe_audio(silent_audio_np)
            print("Warm-up inference complete.")
        except Exception as e:
            print(f"Warm-up inference failed: {e}")
        
        self.model_loaded_event.set()
        print(f"Whisper model ready for transcription.")

        self._running = True
        while self._running:
            try:
                # Continuously extend the audio buffer with new data from the queue
                while not self.transcription_queue.empty():
                    self.audio_buffer.extend(self.transcription_queue.get_nowait())

                # Process the buffer if it has enough data for the transcription interval
                if len(self.audio_buffer) >= interval_buffer_size:
                    # Process all available chunks to catch up
                    while len(self.audio_buffer) >= interval_buffer_size:
                        # Extract the chunk for transcription
                        chunk_to_transcribe = self.audio_buffer[:interval_buffer_size]
                        
                        # Retain the overlap portion for the next chunk
                        self.audio_buffer = self.audio_buffer[interval_buffer_size - overlap_buffer_size:]

                        # Convert byte buffer to a float array that whisper can process
                        audio_np = np.frombuffer(chunk_to_transcribe, dtype=np.int16).astype(np.float32) / 32768.0
                        
                    text = self._transcribe_audio(audio_np)
                    if text:
                        cleaned_text = self._apply_cleanup_strategy(text)
                        if cleaned_text:
                            # Directly send to WordDisplayManager and log
                            self.word_display_manager.add_transcribed_text(cleaned_text)
                            with open(self.log_file_path, "a", encoding="utf-8") as f:
                                f.write(f"{cleaned_text}\n")
                            self._update_transcription_history(cleaned_text)
                else:
                    # If not enough data, wait a bit before checking again
                    threading.Event().wait(0.01) # Small sleep to prevent busy-waiting

            except queue.Empty:
                # This should ideally not be hit often if audio_buffer is processed in a loop
                threading.Event().wait(0.01) # Small sleep to prevent busy-waiting
            except Exception as e:
                print(f"Transcription error: {e}")

    def stop(self):
        self._running = False

    def _update_transcription_history(self, new_text):
        # Add new text to the history, keeping only the most recent part
        self.transcription_history.extend(new_text.split())

    def _apply_cleanup_strategy(self, text):
        if self.cleanup_strategy == "simple_deduplication":
            # Simple de-duplication: remove leading words that are already at the end of the history
            history_str = " ".join(self.transcription_history)
            
            # Find the longest common suffix between history and prefix of new text
            words_in_text = text.split()
            best_match_len = 0
            for i in range(1, min(len(words_in_text), len(self.transcription_history)) + 1):
                if list(self.transcription_history)[-i:] == words_in_text[:i]:
                    best_match_len = i
            
            cleaned_text = " ".join(words_in_text[best_match_len:])
            return cleaned_text.strip()
        return text # No cleanup or unknown strategy

class OpenAIWhisperTranscriber(AbstractTranscriber):
    """
    Transcriber implementation for openai-whisper.
    """
    def _load_model(self):
        import whisper
        self.model = whisper.load_model(self.model_name, device=self.device)
        print(f"OpenAI Whisper model '{self.model_name}' loaded on {self.device}.")
        print(f"  Quantization: {'FP16' if self.device == 'cuda' else 'FP32'}")

    def _transcribe_audio(self, audio_np):
        import time
        start_time = time.time()
        fp16_enabled = (self.device == "cuda")
        result = self.model.transcribe(audio_np, fp16=fp16_enabled)
        inference_time = time.time() - start_time
        print(f"OpenAI Whisper inference time: {inference_time:.2f} seconds")
        return result['text'].strip()

class FasterWhisperTranscriber(AbstractTranscriber):
    """
    Transcriber implementation for faster-whisper.
    """
    def _load_model(self):
        from faster_whisper import WhisperModel
        # Determine compute_type dynamically based on device
        if self.device == "cpu":
            compute_type = "int8"
        elif self.device == "cuda":
            compute_type = "float16"
        else:
            compute_type = "int8" # Default fallback

        self.model = WhisperModel(
            self.model_name, 
            device=self.device, 
            compute_type=compute_type
        )
        print(f"Faster-Whisper model '{self.model_name}' loaded on {self.device} with compute type '{compute_type}'.")
        print(f"  Quantization: {'INT8' if 'int8' in compute_type else 'FP16' if 'float16' in compute_type else 'None'}")
        # Approximate model size based on common Whisper models
        model_sizes = {
            "tiny.en": "75 MB", "tiny": "75 MB",
            "base.en": "140 MB", "base": "140 MB",
            "small.en": "244 MB", "small": "244 MB",
            "medium.en": "769 MB", "medium": "769 MB",
            "large-v1": "1.55 GB", "large-v2": "1.55 GB", "large-v3": "1.55 GB", "large": "1.55 GB",
            "distil-large-v3": "769 MB" # Distil-large-v3 is roughly equivalent to medium size
        }
        print(f"  Approximate model size: {model_sizes.get(self.model_name, 'Unknown')}")


    def _transcribe_audio(self, audio_np):
        import time
        start_time = time.time()
        
        # Prepare initial_prompt from history
        initial_prompt = " ".join(self.transcription_history) if self.transcription_history else None

        segments, _ = self.model.transcribe(
            audio_np,
            vad_filter=self.vad_filter,
            vad_parameters=self.vad_parameters,
            initial_prompt=initial_prompt
        )
        inference_time = time.time() - start_time
        print(f"Faster-Whisper inference time: {inference_time:.2f} seconds")
        # Concatenate segments to form the full text
        return " ".join([segment.text for segment in segments]).strip()
