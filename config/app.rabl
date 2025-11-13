# RABBLE Animated Face Frontend - Main Application Configuration

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

# --- Waveform Base Parameters ---
waveform_config:
  base_frequency: 1.0                   # Base frequency (sine wave cycles per screen width)
  breathing_amplitude: 0.15             # Breathing effect amplitude (0-1)
  line_width: 5                         # Line thickness for drawing

# --- Emotion Configuration File Reference ---
# Emotions are defined in a separate emotions.rabl file for better organization
emotions_file: "emotions.rabl"          # Path relative to this config directory
transcription_file: "transcription.rabl" # Path relative to this config directory
