# Emotion-specific configuration for RABBLE Animated Face Frontend
# Each emotion has its own cycle_rate and waveform frequency

emotion_config:
  IDLE:
    blink_interval: 1000                              # Milliseconds between blinks
    mouth_shape: sine                                 # Shape type: sine, parabolic, saw, default
    y_offset: 0                                       # Vertical offset for mouth
    audio_amplitude_multiplier: 750                    # Controls audio waveform amplitude (0-100 scale)
    cycle_rate: 1.0                                   # Animation cycle rate (1.0 = normal speed)
    shape_params:
      sine_frequency: 3                               # In terms of π (2π radians = one full cycle)
  
  NEUTRAL:
    blink_interval: 800
    mouth_shape: saw
    y_offset: 0
    audio_amplitude_multiplier: 750
    cycle_rate: 1.0                                  # Slightly faster than IDLE
    shape_params:
      saw_frequency: 4                              # In terms of π
  
  HAPPY:
    blink_interval: 1000
    mouth_shape: parabolic
    y_offset: -15
    audio_amplitude_multiplier: 800
    cycle_rate: 0.8                                   # Slower, steady motion
    shape_params:
      parabolic_sine_frequency: 2                   # In terms of π
      curve_direction: 4                            # 1.0 for smile (convex), -1.0 for frown (concave)
  
  ANGRY:
    blink_interval: 2000
    mouth_shape: parabolic
    y_offset: 25
    audio_amplitude_multiplier:    900                # More expressive
    cycle_rate: 3.0                                   # Fast, nervous motion
    shape_params:
      parabolic_sine_frequency: 10                  # In terms of π - faster oscillation
      curve_direction: -4.0                           # Inverted parabola for wide-open mouth
  
  SAD:
    blink_interval: 2000
    mouth_shape: parabolic
    y_offset: 25
    audio_amplitude_multiplier: 800                   # More subdued
    cycle_rate: 0.2                                  # Slower, melancholic motion
    shape_params:
      parabolic_sine_frequency: 2                  # In terms of π
      curve_direction: -3                           # Inverted parabola for sad expression
  