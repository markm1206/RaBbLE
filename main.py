import pygame
import sys
import queue
import numpy as np
import threading
from face import Face
from audio_handler import AudioHandler
from transcriber import OpenAIWhisperTranscriber, FasterWhisperTranscriber

# --- Constants ---
TRANSCRIBER_BACKEND = "faster-whisper"  # Options: "openai", "faster-whisper"
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)  # Black
EYE_COLOR = (150, 75, 150)     # Less saturated magenta
WAVEFORM_COLOR = EYE_COLOR  # Mouth color same as eyes
TEXT_COLOR = (255, 255, 255) # White

EMOTIONS = ["IDLE", "HAPPY", "SAD", "ANGRY"]

def main():
    """Main animation loop."""
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RABBLE - Animated Face with Transcription")
    font = pygame.font.Font(None, 36)

    # --- Queues and Events for Thread Communication ---
    animation_queue = queue.Queue(maxsize=2)
    transcription_queue = queue.Queue()
    text_queue = queue.Queue()
    model_loaded_event = threading.Event()

    # --- Start Audio and Transcription Threads ---
    audio_handler = AudioHandler(animation_queue, transcription_queue)
    
    if TRANSCRIBER_BACKEND == "faster-whisper":
        transcriber = FasterWhisperTranscriber(transcription_queue, text_queue, model_loaded_event)
    else: # Default to openai
        transcriber = OpenAIWhisperTranscriber(transcription_queue, text_queue, model_loaded_event)
        
    audio_handler.start()
    transcriber.start()

    # Create face with inherited colors from constants
    face = Face(WIDTH // 2, HEIGHT // 2, EYE_COLOR, WAVEFORM_COLOR, BACKGROUND_COLOR)
    
    current_emotion_index = 0 # Start with IDLE emotion
    face.set_emotion(EMOTIONS[current_emotion_index])

    running = True
    last_text = "Initializing Transcription..."
    model_ready = False
    normalized_data = np.zeros(1024 * 2) # Initialize with silent data
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    current_emotion_index = (current_emotion_index + 1) % len(EMOTIONS)
                    face.set_emotion(EMOTIONS[current_emotion_index])
                    print(f"Emotion changed to: {face.emotion}")
                elif event.key == pygame.K_t:
                    face.toggle_eyelids()

        face.update()

        screen.fill(BACKGROUND_COLOR)

        current_time = pygame.time.get_ticks()

        try:
            # Get the latest audio data for animation without blocking
            normalized_data = animation_queue.get_nowait()
        except queue.Empty:
            # If the queue is empty, use the last available data to keep animating
            pass
        
        face.draw(screen, normalized_data, current_time)

        # --- Handle Transcription Text ---
        if not model_ready and model_loaded_event.is_set():
            model_ready = True
            last_text = "" # Clear the initializing message

        if model_ready:
            try:
                # Check for new transcribed text
                last_text = text_queue.get_nowait()
            except queue.Empty:
                pass # No new text

        # Render the transcribed text
        text_surface = font.render(last_text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()

    # --- Cleanup ---
    audio_handler.stop()
    transcriber.stop()
    audio_handler.join()
    transcriber.join()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
