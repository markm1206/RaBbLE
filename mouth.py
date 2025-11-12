import pygame
import numpy as np


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

    def draw(self, screen, normalized_data, y_offset, amplitude_multiplier, shape="default", current_time=0, max_amplitude=None):
        """
        Draw the mouth based on audio data.
        
        Args:
            screen: Pygame screen surface
            normalized_data: Normalized audio data array
            y_offset: Vertical offset for the mouth shape
            amplitude_multiplier: Multiplier for audio amplitude
            shape: Shape type ('default', 'parabolic', or 'saw')
            max_amplitude: The maximum vertical distance the waveform can travel from the center
        """
        points = []
        start_index = len(normalized_data) // 2 - (self.width // 2)
        end_index = len(normalized_data) // 2 + (self.width // 2)

        # Time-varied amplitude for subtle breathing effect, ensuring a minimum waveform presence
        time_amplitude_factor = 0.7 + 0.3 * np.sin(current_time * 0.004) # Increased speed

        if shape == "parabolic":
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                curve_factor = 1 - (abs(i - (self.width // 2)) / (self.width // 2))**2
                
                # Add a slight, time-varied sine waveform
                parabolic_sine_frequency = 0.03
                parabolic_sine_amplitude = 5 * time_amplitude_factor
                sine_undulation = parabolic_sine_amplitude * np.sin(i * parabolic_sine_frequency + current_time * 0.005)
                
                y = self.y + y_offset * curve_factor + sample * amplitude_multiplier + sine_undulation
                points.append((x, y))
        elif shape == "saw":
            saw_period = self.width // 8 # Higher frequency
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                pos_in_cycle = (i + int(current_time * 0.02)) % saw_period # Faster time-based movement
                base_amplitude = 20 # Higher minimum amplitude
                if pos_in_cycle < saw_period / 2:
                    saw_offset = base_amplitude + (pos_in_cycle / (saw_period / 2)) * (40 * time_amplitude_factor)
                else:
                    saw_offset = base_amplitude + (1 - ((pos_in_cycle - (saw_period / 2)) / (saw_period / 2))) * (40 * time_amplitude_factor)
                y = self.y - saw_offset + sample * amplitude_multiplier
                points.append((x, y))
        elif shape == "sine":
            # Small undulating sine wave with time-based movement and amplitude
            sine_frequency = 0.05 # Adjust for more or less waves
            sine_amplitude = 10 * time_amplitude_factor # Adjust for height of undulation, time-varied
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                sine_offset = sine_amplitude * (1 + np.sin(i * sine_frequency + current_time * 0.01)) # Increased speed
                y = self.y + y_offset + sine_offset + sample * amplitude_multiplier
                points.append((x, y))
        else:  # Default
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                y = self.y + sample * amplitude_multiplier
                points.append((x, y))

        if max_amplitude is not None:
            final_points = []
            for x, y in points:
                clamped_y = np.clip(y, self.y - max_amplitude, self.y + max_amplitude)
                final_points.append((x, int(clamped_y)))
            points = final_points

        if len(points) > 1:
            pygame.draw.lines(screen, self.color, False, points, 5) # Smoother line
