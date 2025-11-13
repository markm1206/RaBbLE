import pyaudio
import numpy as np
import threading
import queue

class AudioHandler(threading.Thread):
    """
    Handles audio input in a separate thread, providing raw and normalized data
    to separate queues for transcription and real-time animation.
    """
    def __init__(self, animation_queue, transcription_queue, model_loaded_event, chunk_size=1024 * 2, rate=16000, channels=1, format=pyaudio.paInt16, gain_factor=1.5):
        super().__init__()
        self.animation_queue = animation_queue
        self.transcription_queue = transcription_queue
        self.model_loaded_event = model_loaded_event
        self.chunk_size = chunk_size
        self.rate = rate
        self.channels = channels
        self.format = format
        self.gain_factor = gain_factor
        self._running = False
        self.p = pyaudio.PyAudio()
        self.stream = None

    def run(self):
        """
        The main loop of the audio thread. Reads audio from the microphone
        and puts it into the respective queues.
        """
        self._running = True
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk_size)

        print("Audio stream started.")

        while self._running:
            try:
                raw_data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                
                # --- For animation, use the original, un-amplified data ---
                data_for_animation = np.frombuffer(raw_data, dtype=np.int16)
                normalized_data = data_for_animation / (2.**15)
                
                if not self.animation_queue.full():
                    self.animation_queue.put_nowait(normalized_data)

                # --- For transcription, wait for the model to be loaded, then amplify and put into queue ---
                if self.model_loaded_event.is_set():
                    data_for_transcription = np.frombuffer(raw_data, dtype=np.int16)
                    amplified_data = (data_for_transcription * self.gain_factor).astype(np.int16)
                    
                    # Put audio data into the transcription queue (unbounded, so no need to check full or discard)
                    self.transcription_queue.put(amplified_data.tobytes())
                else:
                    # Optionally print a message once when starting to wait for model
                    if not hasattr(self, '_waiting_for_model_printed'):
                        print("Audio handler waiting for model to load before feeding transcription queue...")
                        self._waiting_for_model_printed = True


            except IOError as e:
                print(f"Audio reading error: {e}")
            except queue.Full:
                # This can happen if the main thread is not consuming data fast enough.
                # For animation queue, we'll just continue, effectively dropping the data.
                continue
            except Exception as e:
                print(f"AudioHandler unexpected error: {e}")
                self._running = False


        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

    def stop(self):
        """
        Stops the audio reading thread.
        """
        self._running = False
