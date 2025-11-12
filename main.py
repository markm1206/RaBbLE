import pygame
import sys
import queue
import numpy as np
import threading
from face import Face
from audio_handler import AudioHandler
from transcriber import OpenAIWhisperTranscriber, FasterWhisperTranscriber
from rabl_parser import parse_rabl

def main():
    """Main animation loop."""
    pygame.init()

    # Load all configuration from RABL file in config directory
    # The path is relative to the script's directory, so it will work from anywhere
    config_data = parse_rabl("config/app.rabl")
    
    if config_data is None:
        print("Failed to load configuration. Exiting.")
        return
    
    print("Parsed Configuration Data:")
    print(config_data)
    
    # Extract configuration sections
    display_config = config_data.get('display_config', {})
    colors_config = config_data.get('colors', {})
    face_config = config_data.get('face_config', {})
    audio_config = config_data.get('audio_config', {})
    transcription_config = config_data.get('transcription_config', {})
    waveform_config = config_data.get('waveform_config', {})
    emotion_config_data = config_data.get('emotion_config', {})
    
    # Display settings from RABL
    WIDTH = display_config.get('width', 800)
    HEIGHT = display_config.get('height', 600)
    BACKGROUND_COLOR = tuple(display_config.get('background_color', [0, 0, 0]))
    TEXT_COLOR = tuple(display_config.get('text_color', [255, 255, 255]))
    
    # Color scheme from RABL
    EYE_COLOR = tuple(colors_config.get('eye_color', [150, 75, 150]))
    WAVEFORM_COLOR = tuple(colors_config.get('waveform_color', [150, 75, 150]))
    
    # Audio settings from RABL
    audio_chunk_size = audio_config.get('chunk_size', 2048)
    audio_rate = audio_config.get('sample_rate', 16000)
    audio_channels = audio_config.get('channels', 1)
    audio_gain_factor = audio_config.get('gain_factor', 1.5)
    
    # Transcription settings from RABL
    TRANSCRIBER_BACKEND = transcription_config.get('backend', 'faster-whisper')
    TRANSCRIBER_MODEL = transcription_config.get('model_name', 'tiny.en')
    
    # Get emotions from config
    EMOTIONS = list(emotion_config_data.keys())

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RABBLE - Animated Face with Transcription")
    font = pygame.font.Font(None, 36)

    # --- Queues and Events for Thread Communication ---
    animation_queue = queue.Queue(maxsize=2)
    transcription_queue = queue.Queue()
    text_queue = queue.Queue()
    model_loaded_event = threading.Event()

    # --- Start Audio and Transcription Threads ---
    audio_handler = AudioHandler(animation_queue, transcription_queue, 
                                chunk_size=audio_chunk_size, rate=audio_rate, 
                                channels=audio_channels, gain_factor=audio_gain_factor)
    
    if TRANSCRIBER_BACKEND == "faster-whisper":
        transcriber = FasterWhisperTranscriber(transcription_queue, text_queue, model_loaded_event, model_name=TRANSCRIBER_MODEL)
    else: # Default to openai
        transcriber = OpenAIWhisperTranscriber(transcription_queue, text_queue, model_loaded_event, model_name=TRANSCRIBER_MODEL)
        
    audio_handler.start()
    transcriber.start()

    # Create face with inherited colors from config and pass emotion config
    face = Face(WIDTH // 2, HEIGHT // 2, EYE_COLOR, WAVEFORM_COLOR, BACKGROUND_COLOR, 
               emotion_config_data, face_config, waveform_config)
    
    current_emotion_index = 0 # Start with IDLE emotion
    face.set_emotion(EMOTIONS[current_emotion_index]) # Set initial emotion from loaded config

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
