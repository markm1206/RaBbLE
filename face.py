from eye import Eye
from mouth import Mouth


class Face:
    def __init__(self, x, y, eye_color, mouth_color, background_color, emotion_config, face_config=None, waveform_config=None):
        """
        Initialize a Face component.
        
        Args:
            x: X position of the face center
            y: Y position of the face center
            eye_color: RGB tuple for eye color (inherited from constructor)
            mouth_color: RGB tuple for mouth color (inherited from constructor)
            background_color: RGB tuple for background color
            emotion_config: Dictionary containing emotion configurations loaded from RABL.
            face_config: Dictionary containing face positioning configuration from RABL.
            waveform_config: Dictionary containing waveform configuration from RABL.
        """
        self.x = x
        self.y = y
        self.eye_color = eye_color
        self.mouth_color = mouth_color
        self.background_color = background_color
        self.emotion_config = emotion_config  # Store the emotion configuration
        self.face_config = face_config or {}  # Store face configuration
        self.waveform_config = waveform_config or {}  # Store waveform configuration
        self.emotion = "IDLE"  # Default to IDLE
        
        # Load eye configuration from face_config
        eye_config = self.face_config.get('eye', {})
        eye_radius = eye_config.get('radius', 30)
        left_eye_x_offset = eye_config.get('left_x_offset', -60)
        right_eye_x_offset = eye_config.get('right_x_offset', 60)
        eye_y_offset = eye_config.get('y_offset', -40)
        left_eyelid_pos = eye_config.get('left_eyelid_position', 'bottom')
        right_eyelid_pos = eye_config.get('right_eyelid_position', 'top')
        
        # Create eye components with configuration
        self.left_eye = Eye(x + left_eye_x_offset, y + eye_y_offset, eye_radius, eye_color, background_color, left_eyelid_pos)
        self.right_eye = Eye(x + right_eye_x_offset, y + eye_y_offset, eye_radius, eye_color, background_color, right_eyelid_pos)
        
        # Load mouth configuration from face_config
        mouth_config = self.face_config.get('mouth', {})
        mouth_y_offset = mouth_config.get('y_offset', 80)
        mouth_width = mouth_config.get('width', 300)
        self.max_amplitude = mouth_config.get('max_amplitude', 90)
        
        self.mouth = Mouth(x, y + mouth_y_offset, mouth_width, mouth_color)

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

        # Get current emotion's mouth parameters from config
        config = self.emotion_config.get(self.emotion, {})
        mouth_shape = config.get('mouth_shape', 'default')
        y_offset = config.get('y_offset', 0)
        # Handle both old and new parameter names for backward compatibility
        audio_amplitude_multiplier = config.get('audio_amplitude_multiplier', config.get('amplitude_multiplier', 60))
        cycle_rate = config.get('cycle_rate', 1.0)
        shape_params = config.get('shape_params', {})

        self.mouth.draw(screen, normalized_data, y_offset, audio_amplitude_multiplier, mouth_shape, current_time, 
                       self.max_amplitude, shape_params, self.waveform_config, cycle_rate)
