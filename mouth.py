import pygame
import numpy as np

# --- Waveform Configuration Constants ---
DEFAULT_WAVEFORM_FREQUENCY = 0.05 # Consistent frequency for all waveforms
BREATHING_EFFECT_AMPLITUDE = 0.15 # Reduced amplitude for the breathing effect (was 0.3)

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

    def draw(self, screen, normalized_data, y_offset, amplitude_multiplier, shape="default", current_time=0, max_amplitude=None, shape_params=None):
        """
        Draw the mouth based on audio data.
        
        Args:
            screen: Pygame screen surface
            normalized_data: Normalized audio data array
            y_offset: Vertical offset for the mouth shape
            amplitude_multiplier: Multiplier for audio amplitude
            shape: Shape type ('default', 'parabolic', or 'saw')
            max_amplitude: The maximum vertical distance the waveform can travel from the center
            shape_params: Dictionary of shape-specific parameters from RABL config.
        """
        if shape_params is None:
            shape_params = {}

        points = []
        start_index = len(normalized_data) // 2 - (self.width // 2)
        end_index = len(normalized_data) // 2 + (self.width // 2)

        # Time-varied amplitude for subtle breathing effect, ensuring a minimum waveform presence
        # Reduced amplitude for the breathing effect
        time_amplitude_factor = 0.7 + BREATHING_EFFECT_AMPLITUDE * np.sin(current_time * 0.004)

        if shape == "parabolic":
            parabolic_sine_frequency = shape_params.get('parabolic_sine_frequency', DEFAULT_WAVEFORM_FREQUENCY)
            parabolic_sine_amplitude = shape_params.get('parabolic_sine_amplitude', 5) * time_amplitude_factor
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                curve_factor = 1 - (abs(i - (self.width // 2)) / (self.width // 2))**2
                
                sine_undulation = parabolic_sine_amplitude * np.sin(i * parabolic_sine_frequency + current_time * DEFAULT_WAVEFORM_FREQUENCY)
                
                y = self.y + y_offset * curve_factor + sample * amplitude_multiplier + sine_undulation
                points.append((x, y))
        elif shape == "saw":
            saw_period_divisor = shape_params.get('saw_period_divisor', 8)
            base_amplitude = shape_params.get('base_amplitude', 20)
            saw_period = self.width // saw_period_divisor
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                pos_in_cycle = (i + int(current_time * DEFAULT_WAVEFORM_FREQUENCY * 2)) % saw_period # Use default frequency
                
                if pos_in_cycle < saw_period / 2:
                    saw_offset = base_amplitude + (pos_in_cycle / (saw_period / 2)) * (40 * time_amplitude_factor)
                else:
                    saw_offset = base_amplitude + (1 - ((pos_in_cycle - (saw_period / 2)) / (saw_period / 2))) * (40 * time_amplitude_factor)
                y = self.y - saw_offset + sample * amplitude_multiplier
                points.append((x, y))
        elif shape == "sine":
            sine_frequency = shape_params.get('sine_frequency', DEFAULT_WAVEFORM_FREQUENCY)
            sine_amplitude = shape_params.get('sine_amplitude', 10) * time_amplitude_factor
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                sine_offset = sine_amplitude * (1 + np.sin(i * sine_frequency + current_time * DEFAULT_WAVEFORM_FREQUENCY)) # Use default frequency
                y = self.y + y_offset + sine_offset + sample * amplitude_multiplier
                points.append((x, y))
        else:  # Default
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                y = self.y + y_offset + sample * amplitude_multiplier # Apply y_offset to default shape
                points.append((x, y))

        if max_amplitude is not None:
            final_points = []
            for x, y in points:
                clamped_y = np.clip(y, self.y - max_amplitude, self.y + max_amplitude)
                final_points.append((x, int(clamped_y)))
            points = final_points

        if len(points) > 1:
            pygame.draw.lines(screen, self.color, False, points, 5) # Smoother line
