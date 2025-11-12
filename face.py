from eye import Eye
from mouth import Mouth


class Face:
    def __init__(self, x, y, eye_color, mouth_color, background_color):
        """
        Initialize a Face component.
        
        Args:
            x: X position of the face center
            y: Y position of the face center
            eye_color: RGB tuple for eye color (inherited from constructor)
            mouth_color: RGB tuple for mouth color (inherited from constructor)
            background_color: RGB tuple for background color
        """
        self.x = x
        self.y = y
        self.eye_color = eye_color
        self.mouth_color = mouth_color
        self.background_color = background_color
        self.emotion = "HAPPY"
        
        # Create eye and mouth components with inherited colors
        eye_radius = 30
        self.left_eye = Eye(x - 60, y - 40, eye_radius, eye_color, background_color, 'bottom')
        self.right_eye = Eye(x + 60, y - 40, eye_radius, eye_color, background_color, 'top')
        self.mouth = Mouth(x, y + 80, 300, mouth_color)

    def set_emotion(self, emotion):
        """Set the face emotion and update blink intervals accordingly."""
        self.emotion = emotion
        if self.emotion == "ANGRY":
            self.left_eye.set_blink_interval(500)
            self.right_eye.set_blink_interval(500)
        elif self.emotion == "SAD":
            self.left_eye.set_blink_interval(2000)
            self.right_eye.set_blink_interval(2000)
        else:  # HAPPY
            self.left_eye.set_blink_interval(1000)
            self.right_eye.set_blink_interval(1000)

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
        """Draw the face with its current emotion."""
        self.left_eye.draw(screen)
        self.right_eye.draw(screen)

        if self.emotion == "SAD":
            self.mouth.draw(screen, normalized_data, -40, 500, "parabolic", current_time)
        elif self.emotion == "HAPPY":
            self.mouth.draw(screen, normalized_data, 40, 500, "parabolic", current_time)
        elif self.emotion == "ANGRY":
            self.mouth.draw(screen, normalized_data, 0, 800, "saw", current_time)
        elif self.emotion == "IDLE":
            self.mouth.draw(screen, normalized_data, 0, 200, "sine", current_time) # Subtle sine wave for idle
        else:
            self.mouth.draw(screen, normalized_data, 0, 500, "default", current_time)
