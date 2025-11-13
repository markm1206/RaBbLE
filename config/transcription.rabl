# RABBLE Animated Face Frontend - Transcription Configuration

transcription_config:
  interval_seconds: 2.0             # How often to process transcription
  overlap_seconds: 0.1                 # Overlap between chunks
  backend: "faster-whisper"             # Options: "openai", "faster-whisper"
  model_name: "distil-large-v3"                 # Whisper model name (e.g., "tiny.en", "base.en", "small.en", "medium.en", "large-v3", "distil-large-v3")
  device: "cuda"                         # Options: "cpu", "cuda" (if GPU available)
  vad_filter: true                      # Enable Voice Activity Detection
  vad_parameters:                       # Parameters for VAD filter
    min_silence_duration_ms: 500        # Minimum silence duration to consider as non-speech
  transcription_history_size: 500       # Number of characters to keep for initial_prompt context
  cleanup_strategy: "simple_deduplication" # Options: "simple_deduplication", "none"

  # --- Word Display Configuration ---
  scroll_speed: 180                     # Pixels per second for word scrolling
  word_display_interval_ms: 150         # Milliseconds between each new word appearing
  display_text_y_offset: 50             # Vertical offset from the bottom of the screen for text
