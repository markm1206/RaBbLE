# RABBLE Animated Face Frontend - Audio Configuration

audio_config:
  chunk_size: 2048                      # PyAudio chunk size (1024 * 2)
  sample_rate: 16000                    # Sample rate in Hz
  channels: 1                           # Mono
  gain_factor: 3.0                      # Audio amplification for transcription

waveform_config:
  base_frequency: 1.0                   # Base frequency (sine wave cycles per screen width)
  breathing_amplitude: 0.15             # Breathing effect amplitude (0-1)
  line_width: 5                         # Line thickness for drawing
