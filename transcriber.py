import threading
import queue
import numpy as np
import torch
import os
from datetime import datetime

try:
    import whisper
except ImportError:
    print("Whisper not installed. Please install it with: pip install openai-whisper")
    whisper = None

class WhisperTranscriber(threading.Thread):
    """
    Transcribes audio from a queue using the Whisper model in a separate thread.
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

    def run(self):
        """
        The main loop of the transcriber thread.
        """
        if whisper:
            print("Loading Whisper model...")
            self.model = whisper.load_model(self.model_name)
            self.model_loaded_event.set() # Signal that the model is loaded
            print("Whisper model loaded.")
        else:
            print("Whisper model not loaded. Transcription disabled.")
            return

        self._running = True
        while self._running:
            try:
                # Get all available audio data from the queue to process in a batch
                while not self.transcription_queue.empty():
                    self.audio_buffer.extend(self.transcription_queue.get_nowait())

                # Process the buffer if it has 0.5 seconds of audio data
                if len(self.audio_buffer) > self.sample_rate: # Process every half-second
                    # Convert byte buffer to a float array that whisper can process
                    audio_np = np.frombuffer(self.audio_buffer, dtype=np.int16).astype(np.float32) / 32768.0
                    
                    # Clear the buffer for the next chunk
                    self.audio_buffer.clear()

                    # Transcribe
                    result = self.model.transcribe(audio_np, fp16=torch.cuda.is_available())
                    text = result['text'].strip()

                    if text:
                        self.text_queue.put(text)
                        # --- Log to File ---
                        with open(self.log_file_path, "a", encoding="utf-8") as f:
                            f.write(f"{text}\n")

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Transcription error: {e}")

    def stop(self):
        """
        Stops the transcriber thread.
        """
        self._running = False
