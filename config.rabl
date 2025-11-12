# Emotion configuration for the RABBLE Animated Face Frontend

# --- Display Configuration ---
display_config:
  width: 800
  height: 600
  background_color: [0, 0, 0]           # Black
  text_color: [255, 255, 255]           # White

# --- Color Scheme ---
colors:
  eye_color: [150, 75, 150]             # Less saturated magenta
  waveform_color: [150, 75, 150]        # Same as eye color

# --- Face & Component Positioning ---
face_config:
  # Position relative to screen center
  x_offset: 0                           # Center by default
  y_offset: 0                           # Center by default
  
  # Eye configuration
  eye:
    radius: 30
    left_x_offset: -60                  # Offset from face center
    right_x_offset: 60                  # Offset from face center
    y_offset: -40                       # Offset from face center
    left_eyelid_position: bottom
    right_eyelid_position: top
  
  # Mouth configuration
  mouth:
    y_offset: 80                        # Offset from face center
    width: 300                          # Width of mouth
    max_amplitude: 90                   # Max vertical distance from mouth center

# --- Audio Configuration ---
audio_config:
  chunk_size: 2048                      # PyAudio chunk size (1024 * 2)
  sample_rate: 16000                    # Sample rate in Hz
  channels: 1                           # Mono
  gain_factor: 1.5                      # Audio amplification for transcription

# --- Transcription Configuration ---
transcription_config:
  interval_seconds: 0.5                 # How often to process transcription
  overlap_seconds: 0.1                  # Overlap between chunks
  backend: "faster-whisper"             # Options: "openai", "faster-whisper"
  model_name: "tiny.en"                 # Whisper model name

# --- Waveform Base Parameters ---
waveform_config:
  base_frequency: 1.0                   # Base frequency (sine wave cycles per screen width)
  breathing_amplitude: 0.15             # Breathing effect amplitude (0-1)
  line_width: 5                         # Line thickness for drawing

# --- Emotion Configuration ---
emotion_config:
  IDLE:
    blink_interval: 1000
    mouth_shape: sine
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      sine_frequency: 0.015             # Reduced frequency (0.015 * base_frequency)
      sine_amplitude: 10
  HAPPY:
    blink_interval: 1000
    mouth_shape: parabolic
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      parabolic_sine_frequency: 0.05    # Relative to base frequency
      parabolic_sine_amplitude: 5
      curve_factor_intensity: 1.0       # Intensity of parabolic curvature
  SAD:
    blink_interval: 2000
    mouth_shape: parabolic
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      parabolic_sine_frequency: 0.05
      parabolic_sine_amplitude: 5
      curve_factor_intensity: 1.0
  ANGRY:
    blink_interval: 500
    mouth_shape: saw
    y_offset: 0
    amplitude_multiplier: 700
    shape_params:
      saw_period_divisor: 8
      base_amplitude: 20
      saw_frequency: 0.02                # Frequency of sawtooth oscillation
