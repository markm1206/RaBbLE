# Emotion configuration for the RABBLE Animated Face Frontend

emotion_config:
  IDLE:
    blink_interval: 1000
    mouth_shape: sine
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      sine_frequency: 0.015 # Reduced frequency for a slower, more subtle animation
      sine_amplitude: 10
  HAPPY:
    blink_interval: 1000
    mouth_shape: parabolic
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      parabolic_sine_frequency: 0.05 # Standardized frequency
      parabolic_sine_amplitude: 5
  SAD:
    blink_interval: 2000
    mouth_shape: parabolic
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      parabolic_sine_frequency: 0.05 # Standardized frequency
      parabolic_sine_amplitude: 5
  ANGRY:
    blink_interval: 500
    mouth_shape: saw
    y_offset: 0
    amplitude_multiplier: 700
    shape_params:
      saw_period_divisor: 8
