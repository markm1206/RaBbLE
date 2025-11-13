import pygame
import sys
import queue
import numpy as np
import threading
from collections import deque # Needed for WordDisplayManager
import time # Needed for delta_time calculation
import signal # For graceful shutdown
from src.animation.face import Face
from src.audio.audio_handler import AudioHandler
from src.transcription.transcriber import OpenAIWhisperTranscriber, FasterWhisperTranscriber, print_supported_gpu_devices
# from src.config.rabl_parser import parse_rabl # No longer directly used
from src.ui.word_display_manager import WordDisplayManager
from src.config.config_loader import ConfigLoader

def main():
    """Main animation loop."""
    pygame.init()

    # Load all configuration using the new ConfigLoader
    config_loader = ConfigLoader()
    config = config_loader.load_config()
    
    if not config:
        print("Failed to load configuration. Exiting.")
        return
    
    config_loader.print_config()
    
    # Display settings from ConfigLoader
    WIDTH = config_loader.get('display_config.width', 800)
    HEIGHT = config_loader.get('display_config.height', 600)
    BACKGROUND_COLOR = tuple(config_loader.get('display_config.background_color', [0, 0, 0]))
    TEXT_COLOR = tuple(config_loader.get('display_config.text_color', [255, 255, 255]))
    
    # Color scheme from ConfigLoader
    EYE_COLOR = tuple(config_loader.get('colors.eye_color', [150, 75, 150]))
    WAVEFORM_COLOR = tuple(config_loader.get('colors.waveform_color', [150, 75, 150]))
    
    # Audio settings from ConfigLoader
    audio_chunk_size = config_loader.get('audio_config.chunk_size', 2048)
    audio_rate = config_loader.get('audio_config.sample_rate', 16000)
    audio_channels = config_loader.get('audio_config.channels', 1)
    audio_gain_factor = config_loader.get('audio_config.gain_factor', 1.5)
    
    # Transcription settings from ConfigLoader
    TRANSCRIBER_BACKEND = config_loader.get('transcription_config.backend', 'faster-whisper')
    TRANSCRIBER_MODEL = config_loader.get('transcription_config.model_name', 'tiny.en')
    TRANSCRIBER_DEVICE = config_loader.get('transcription_config.device', 'cpu')
    TRANSCRIPTION_INTERVAL_SECONDS = config_loader.get('transcription_config.interval_seconds', 0.5)
    OVERLAP_SECONDS = config_loader.get('transcription_config.overlap_seconds', 0.1)
    VAD_FILTER = config_loader.get('transcription_config.vad_filter', False)
    VAD_PARAMETERS = config_loader.get('transcription_config.vad_parameters', {})
    TRANSCRIPTION_HISTORY_SIZE = config_loader.get('transcription_config.transcription_history_size', 50)
    CLEANUP_STRATEGY = config_loader.get('transcription_config.cleanup_strategy', 'none')

    # Word Display settings from ConfigLoader
    SCROLL_SPEED = config_loader.get('transcription_config.scroll_speed', 70)
    WORD_DISPLAY_INTERVAL_MS = config_loader.get('transcription_config.word_display_interval_ms', 150)
    DISPLAY_TEXT_Y_OFFSET = config_loader.get('transcription_config.display_text_y_offset', 50)
    TEXT_START_OFFSET = config_loader.get('transcription_config.text_start_offset', 50) # New config for text offset
    
    # Get emotions from config
    EMOTIONS = list(config_loader.get('emotion_config', {}).keys())

    # Print supported GPU devices at startup
    print_supported_gpu_devices()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RABBLE - Animated Face with Transcription")
    font = pygame.font.Font(None, 36)

    # --- Queues and Events for Thread Communication ---
    animation_queue = queue.Queue(maxsize=2)
    transcription_queue = queue.Queue()
    model_loaded_event = threading.Event() # For AudioHandler to wait for Transcriber
    transcriber_ready_event = threading.Event() # For WordDisplayManager to know when transcriber is ready

    # Queue for transcribed text to be sent to WordDisplayManager
    transcribed_text_queue = queue.Queue()

    # Initialize WordDisplayManager
    word_display_manager = WordDisplayManager(
        font=font,
        text_color=TEXT_COLOR,
        screen_width=WIDTH,
        screen_height=HEIGHT,
        scroll_speed=SCROLL_SPEED,
        word_display_interval_ms=WORD_DISPLAY_INTERVAL_MS,
        display_text_y_offset=DISPLAY_TEXT_Y_OFFSET,
        transcribed_text_queue=transcribed_text_queue,
        text_start_offset=TEXT_START_OFFSET,
        transcriber_ready_event=transcriber_ready_event # Pass the new event
    )

    # --- Start Audio and Transcription Threads ---
    audio_handler = AudioHandler(animation_queue, transcription_queue, model_loaded_event,
                                chunk_size=audio_chunk_size, rate=audio_rate, 
                                channels=audio_channels, gain_factor=audio_gain_factor)
    
    if TRANSCRIBER_BACKEND == "faster-whisper":
        transcriber = FasterWhisperTranscriber(transcription_queue, transcribed_text_queue, model_loaded_event, 
                                               transcriber_ready_event, # Pass the new event
                                               model_name=TRANSCRIBER_MODEL, device=TRANSCRIBER_DEVICE, 
                                               interval_seconds=TRANSCRIPTION_INTERVAL_SECONDS, 
                                               overlap_seconds=OVERLAP_SECONDS,
                                               transcription_history_size=TRANSCRIPTION_HISTORY_SIZE,
                                               cleanup_strategy=CLEANUP_STRATEGY)
        transcriber.vad_filter = VAD_FILTER
        transcriber.vad_parameters = VAD_PARAMETERS
    else: # Default to openai
        transcriber = OpenAIWhisperTranscriber(transcription_queue, transcribed_text_queue, model_loaded_event, 
                                              transcriber_ready_event, # Pass the new event
                                              model_name=TRANSCRIBER_MODEL, device=TRANSCRIBER_DEVICE, 
                                              interval_seconds=TRANSCRIPTION_INTERVAL_SECONDS, 
                                              overlap_seconds=OVERLAP_SECONDS,
                                              transcription_history_size=TRANSCRIPTION_HISTORY_SIZE,
                                              cleanup_strategy=CLEANUP_STRATEGY)
        
    audio_handler.start()
    transcriber.start()

    # The main loop will now handle drawing the loading message via WordDisplayManager
    # No blocking wait here.
    print("Transcription model loading in background...")

    # Create face with inherited colors from config and pass emotion config
    face = Face(WIDTH // 2, HEIGHT // 2, config_loader)
    
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
