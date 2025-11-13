import threading
import queue
import numpy as np
import torch
import os
from datetime import datetime
from abc import ABC, abstractmethod

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
    def __init__(self, transcription_queue, text_queue, model_loaded_event, 
                 model_name="tiny.en", sample_rate=44100, device="cpu",
                 interval_seconds=0.5, overlap_seconds=0.1):
        super().__init__()
        self.transcription_queue = transcription_queue
        self.text_queue = text_queue
        self.model_loaded_event = model_loaded_event
        self.model_name = model_name
        self.sample_rate = sample_rate
        self.device = device
        self.interval_seconds = interval_seconds
        self.overlap_seconds = overlap_seconds
        # VAD parameters will be handled directly by FasterWhisperTranscriber
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
        self.model_loaded_event.set()
        print(f"Whisper model loaded on {self.device}.")

        self._running = True
        while self._running:
            try:
                # Continuously extend the audio buffer with new data
                while not self.transcription_queue.empty():
                    self.audio_buffer.extend(self.transcription_queue.get_nowait())

                # Process the buffer if it has enough data for the transcription interval
                if len(self.audio_buffer) >= interval_buffer_size:
                    # Extract the chunk for transcription
                    chunk_to_transcribe = self.audio_buffer[:interval_buffer_size]
                    
                    # Retain the overlap portion for the next chunk
                    self.audio_buffer = self.audio_buffer[interval_buffer_size - overlap_buffer_size:]

                    # Convert byte buffer to a float array that whisper can process
                    audio_np = np.frombuffer(chunk_to_transcribe, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    text = self._transcribe_audio(audio_np)
                    if text:
                        self.text_queue.put(text)
                        with open(self.log_file_path, "a", encoding="utf-8") as f:
                            f.write(f"{text}\n")

            except queue.Empty:
                # If the queue is empty, wait a bit before checking again
                threading.Event().wait(0.01) # Small sleep to prevent busy-waiting
            except Exception as e:
                print(f"Transcription error: {e}")

    def stop(self):
        self._running = False

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
        segments, _ = self.model.transcribe(
            audio_np,
            vad_filter=self.vad_filter,
            vad_parameters=self.vad_parameters
        )
        inference_time = time.time() - start_time
        print(f"Faster-Whisper inference time: {inference_time:.2f} seconds")
        # Concatenate segments to form the full text
        return " ".join([segment.text for segment in segments]).strip()
