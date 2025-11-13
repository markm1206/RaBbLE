# RABBLE Animated Face Frontend - Transcription Configuration

transcription_config:
  interval_seconds: 1.0                # How often to process transcription
  overlap_seconds: 0.0                 # Overlap between chunks
  backend: "faster-whisper"          # Options: "openai", "faster-whisper"
  model_name: "large-v3"                 # Whisper model name
  device: "cuda"                         # Options: "cpu", "cuda" (if GPU available)
