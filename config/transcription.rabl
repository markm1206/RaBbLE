# RABBLE Animated Face Frontend - Transcription Configuration

transcription_config:
  interval_seconds: 1.0                # How often to process transcription
  overlap_seconds: 0.2                  # Overlap between chunks
  backend: "faster-whisper"             # Options: "openai", "faster-whisper"
  model_name: "tiny.en"                # Whisper model name (e.g., "tiny.en", "base.en", "small.en", "medium.en", "large-v3", "distil-large-v3")
  device: "cuda"                         # Options: "cpu", "cuda" (if GPU available)
  vad_filter: true                      # Enable Voice Activity Detection
  vad_parameters:                       # Parameters for VAD filter
    min_silence_duration_ms: 500        # Minimum silence duration to consider as non-speech
