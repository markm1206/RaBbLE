import pygame
import sys
import queue
import numpy as np
import threading
from collections import deque # Needed for WordDisplayManager
import time # Needed for delta_time calculation
import signal # For graceful shutdown
from face import Face
from audio_handler import AudioHandler
from transcriber import OpenAIWhisperTranscriber, FasterWhisperTranscriber, print_supported_gpu_devices
from rabl_parser import parse_rabl
from word_display_manager import WordDisplayManager # Import the new class

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
    waveform_config = config_data.get('waveform_config', {})
    emotion_config_data = config_data.get('emotion_config', {})
    transcription_config = config_data.get('transcription_config', {}) # Now loaded from separate file
    
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
    TRANSCRIBER_DEVICE = transcription_config.get('device', 'cpu')
    TRANSCRIPTION_INTERVAL_SECONDS = transcription_config.get('interval_seconds', 0.5)
    OVERLAP_SECONDS = transcription_config.get('overlap_seconds', 0.1)
    VAD_FILTER = transcription_config.get('vad_filter', False)
    VAD_PARAMETERS = transcription_config.get('vad_parameters', {})
    TRANSCRIPTION_HISTORY_SIZE = transcription_config.get('transcription_history_size', 50)
    CLEANUP_STRATEGY = transcription_config.get('cleanup_strategy', 'none')

    # Word Display settings from RABL
    SCROLL_SPEED = transcription_config.get('scroll_speed', 70)
    WORD_DISPLAY_INTERVAL_MS = transcription_config.get('word_display_interval_ms', 150)
    DISPLAY_TEXT_Y_OFFSET = transcription_config.get('display_text_y_offset', 50)
    
    # Get emotions from config
    EMOTIONS = list(emotion_config_data.keys())

    # Print supported GPU devices at startup
    print_supported_gpu_devices()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RABBLE - Animated Face with Transcription")
    font = pygame.font.Font(None, 36)

    # --- Queues and Events for Thread Communication ---
    animation_queue = queue.Queue(maxsize=2)
    transcription_queue = queue.Queue() # Revert to unbounded queue
    # text_queue is no longer needed as Transcriber will directly interact with WordDisplayManager
    model_loaded_event = threading.Event()

    # Initialize WordDisplayManager
    word_display_manager = WordDisplayManager(
        font=font,
        text_color=TEXT_COLOR,
        screen_width=WIDTH,
        screen_height=HEIGHT,
        scroll_speed=SCROLL_SPEED,
        word_display_interval_ms=WORD_DISPLAY_INTERVAL_MS,
        display_text_y_offset=DISPLAY_TEXT_Y_OFFSET
    )

    # --- Start Audio and Transcription Threads ---
    audio_handler = AudioHandler(animation_queue, transcription_queue, model_loaded_event,
                                chunk_size=audio_chunk_size, rate=audio_rate, 
                                channels=audio_channels, gain_factor=audio_gain_factor)
    
    if TRANSCRIBER_BACKEND == "faster-whisper":
        transcriber = FasterWhisperTranscriber(transcription_queue, word_display_manager, model_loaded_event, 
                                               model_name=TRANSCRIBER_MODEL, device=TRANSCRIBER_DEVICE, 
                                               interval_seconds=TRANSCRIPTION_INTERVAL_SECONDS, 
                                               overlap_seconds=OVERLAP_SECONDS,
                                               transcription_history_size=TRANSCRIPTION_HISTORY_SIZE,
                                               cleanup_strategy=CLEANUP_STRATEGY)
        transcriber.vad_filter = VAD_FILTER
        transcriber.vad_parameters = VAD_PARAMETERS
    else: # Default to openai
        transcriber = OpenAIWhisperTranscriber(transcription_queue, word_display_manager, model_loaded_event, 
                                              model_name=TRANSCRIBER_MODEL, device=TRANSCRIBER_DEVICE, 
                                              interval_seconds=TRANSCRIPTION_INTERVAL_SECONDS, 
                                              overlap_seconds=OVERLAP_SECONDS,
                                              transcription_history_size=TRANSCRIPTION_HISTORY_SIZE,
                                              cleanup_strategy=CLEANUP_STRATEGY)
        # OpenAI Whisper does not have built-in VAD like Faster-Whisper, so VAD parameters are not used directly.
        
    audio_handler.start()
    transcriber.start()

    # Create face with inherited colors from config and pass emotion config
    face = Face(WIDTH // 2, HEIGHT // 2, EYE_COLOR, WAVEFORM_COLOR, BACKGROUND_COLOR, 
               emotion_config_data, face_config, waveform_config)
    
    current_emotion_index = 0 # Start with IDLE emotion
    face.set_emotion(EMOTIONS[current_emotion_index]) # Set initial emotion from loaded config

    running = True
    
    # Define signal handler for graceful shutdown
    def signal_handler(sig, frame):
        nonlocal running
        print("SIGINT received, gracefully shutting down...")
        running = False
    
    signal.signal(signal.SIGINT, signal_handler)

    last_frame_time = time.time() # For delta_time calculation
    normalized_data = np.zeros(1024 * 2) # Initialize with silent data
    while running:
        current_time = time.time()
        delta_time = (current_time - last_frame_time) * 1000 # in milliseconds
        last_frame_time = current_time

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

        try:
            # Get the latest audio data for animation without blocking
            normalized_data = animation_queue.get_nowait()
        except queue.Empty:
            # If the queue is empty, use the last available data to keep animating
            pass
        
        face.draw(screen, normalized_data, pygame.time.get_ticks()) # Pass pygame.time.get_ticks() for waveform animation

        # --- Handle Transcription Text (now handled directly by Transcriber) ---
        word_display_manager.update(delta_time)
        word_display_manager.draw(screen)

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
