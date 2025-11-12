import threading
import queue
import numpy as np
import torch
import os
from datetime import datetime
from abc import ABC, abstractmethod

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
        self._load_model()
        self.model_loaded_event.set()
        print("Whisper model loaded.")

        self._running = True
        while self._running:
            try:
                while not self.transcription_queue.empty():
                    self.audio_buffer.extend(self.transcription_queue.get_nowait())

                if len(self.audio_buffer) > self.sample_rate:
                    audio_np = np.frombuffer(self.audio_buffer, dtype=np.int16).astype(np.float32) / 32768.0
                    self.audio_buffer.clear()

                    text = self._transcribe_audio(audio_np)
                    if text:
                        self.text_queue.put(text)
                        with open(self.log_file_path, "a", encoding="utf-8") as f:
                            f.write(f"{text}\n")

            except queue.Empty:
                continue
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
