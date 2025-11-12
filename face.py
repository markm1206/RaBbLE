from eye import Eye
from mouth import Mouth


class Face:
    def __init__(self, x, y, eye_color, mouth_color, background_color, emotion_config):
        """
        Initialize a Face component.
        
        Args:
            x: X position of the face center
            y: Y position of the face center
            eye_color: RGB tuple for eye color (inherited from constructor)
            mouth_color: RGB tuple for mouth color (inherited from constructor)
            background_color: RGB tuple for background color
            emotion_config: Dictionary containing emotion configurations loaded from RABL.
        """
        self.x = x
        self.y = y
        self.eye_color = eye_color
        self.mouth_color = mouth_color
        self.background_color = background_color
        self.emotion_config = emotion_config # Store the emotion configuration
        self.emotion = "IDLE" # Default to IDLE
        
        # Create eye and mouth components with inherited colors
        eye_radius = 30
        self.left_eye = Eye(x - 60, y - 40, eye_radius, eye_color, background_color, 'bottom')
        self.right_eye = Eye(x + 60, y - 40, eye_radius, eye_color, background_color, 'top')
        self.mouth = Mouth(x, y + 80, 300, mouth_color)

    def set_emotion(self, emotion):
        """Set the face emotion and update blink intervals accordingly from config."""
        if emotion in self.emotion_config:
            self.emotion = emotion
            config = self.emotion_config[self.emotion]
            blink_interval = config.get('blink_interval', 1000) # Default to 1000ms if not specified
            self.left_eye.set_blink_interval(blink_interval)
            self.right_eye.set_blink_interval(blink_interval)
        else:
            print(f"Warning: Emotion '{emotion}' not found in configuration.")

    def toggle_eyelids(self):
        """Toggle the eyelid positions."""
        if self.left_eye.eyelid_position == 'bottom':
            self.left_eye.set_eyelid_position('top')
            self.right_eye.set_eyelid_position('bottom')
        else:
            self.left_eye.set_eyelid_position('bottom')
            self.right_eye.set_eyelid_position('top')

    def update(self):
        """Update the face components."""
        self.left_eye.update()
        self.right_eye.update()

    def draw(self, screen, normalized_data, current_time):
        """Draw the face with its current emotion, using parameters from config."""
        self.left_eye.draw(screen)
        self.right_eye.draw(screen)

        max_amplitude = 90 # The vertical distance from mouth center to bottom of eyes

        # Get current emotion's mouth parameters from config
        config = self.emotion_config.get(self.emotion, {})
        mouth_shape = config.get('mouth_shape', 'default')
        y_offset = config.get('y_offset', 0)
        amplitude_multiplier = config.get('amplitude_multiplier', 600)
        shape_params = config.get('shape_params', {})

        self.mouth.draw(screen, normalized_data, y_offset, amplitude_multiplier, mouth_shape, current_time, max_amplitude, shape_params)
