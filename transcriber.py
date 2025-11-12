import threading
import queue
import numpy as np
import torch
import os
from datetime import datetime
from abc import ABC, abstractmethod

# --- Transcriber Configuration Constants ---
TRANSCRIPTION_INTERVAL_SECONDS = 0.5 # How often to attempt transcription
OVERLAP_SECONDS = 0.1 # How much audio to overlap between transcription chunks

class AbstractTranscriber(ABC, threading.Thread):
    """
    Abstract base class for transcriber implementations.
    """
    def __init__(self, transcription_queue, text_queue, model_loaded_event, model_name="tiny.en", sample_rate=44100):
        super().__init__()
        self.transcription_queue = transcription_queue
        self.text_queue = text_queue
        self.model_loaded_event = model_loaded_event
        self.model_name = model_name
        self.sample_rate = sample_rate
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
        # Calculate buffer sizes in bytes
        interval_buffer_size = int(self.sample_rate * TRANSCRIPTION_INTERVAL_SECONDS) * 2 # 2 bytes per int16 sample
        overlap_buffer_size = int(self.sample_rate * OVERLAP_SECONDS) * 2 # 2 bytes per int16 sample

        self._load_model()
        self.model_loaded_event.set()
        print("Whisper model loaded.")

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
        self.model = whisper.load_model(self.model_name)

    def _transcribe_audio(self, audio_np):
        result = self.model.transcribe(audio_np, fp16=torch.cuda.is_available())
        return result['text'].strip()

class FasterWhisperTranscriber(AbstractTranscriber):
    """
    Transcriber implementation for faster-whisper.
    """
    def _load_model(self):
        from faster_whisper import WhisperModel
        # Use "int8" for faster CPU performance
        self.model = WhisperModel(self.model_name, device="cpu", compute_type="int8")

    def _transcribe_audio(self, audio_np):
        segments, _ = self.model.transcribe(audio_np)
        # Concatenate segments to form the full text
        return " ".join([segment.text for segment in segments]).strip()
