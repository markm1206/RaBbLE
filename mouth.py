import pygame


class Mouth:
    def __init__(self, x, y, width, color):
        """
        Initialize a Mouth component.
        
        Args:
            x: X position of the mouth center
            y: Y position of the mouth center
            width: Width of the mouth
            color: RGB tuple for the mouth color (inherited from constructor)
        """
        self.x = x
        self.y = y
        self.width = width
        self.color = color

    def draw(self, screen, normalized_data, y_offset, amplitude_multiplier, shape="default"):
        """
        Draw the mouth based on audio data.
        
        Args:
            screen: Pygame screen surface
            normalized_data: Normalized audio data array
            y_offset: Vertical offset for the mouth shape
            amplitude_multiplier: Multiplier for audio amplitude
            shape: Shape type ('default', 'parabolic', or 'saw')
        """
        points = []
        start_index = len(normalized_data) // 2 - (self.width // 2)
        end_index = len(normalized_data) // 2 + (self.width // 2)
        
        if shape == "parabolic":
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                curve_factor = 1 - (abs(i - (self.width // 2)) / (self.width // 2))**2
                y = int(self.y + y_offset * curve_factor + sample * amplitude_multiplier)
                points.append((x, y))
        elif shape == "saw":
            saw_period = self.width // 4
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                pos_in_cycle = i % saw_period
                if pos_in_cycle < saw_period / 2:
                    saw_offset = (pos_in_cycle / (saw_period / 2)) * 40
                else:
                    saw_offset = (1 - ((pos_in_cycle - (saw_period / 2)) / (saw_period / 2))) * 40
                y = int(self.y - saw_offset + sample * amplitude_multiplier)
                points.append((x, y))
        else:  # Default
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                y = int(self.y + sample * amplitude_multiplier)
                points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, self.color, False, points, 4)
