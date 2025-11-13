# RABBLE Animated Face Frontend - Face & Component Positioning

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
