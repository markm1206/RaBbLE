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

    def draw(self, screen, normalized_data, y_offset, amplitude_multiplier, shape="default", 
             current_time=0, max_amplitude=None, shape_params=None, waveform_config=None):
        """
        Draw the mouth based on audio data.
        
        Args:
            screen: Pygame screen surface
            normalized_data: Normalized audio data array
            y_offset: Vertical offset for the mouth shape
            amplitude_multiplier: Multiplier for audio amplitude
            shape: Shape type ('default', 'parabolic', 'sine', or 'saw')
            current_time: Current time in milliseconds (from pygame.time.get_ticks())
            max_amplitude: The maximum vertical distance the waveform can travel from the center
            shape_params: Dictionary of shape-specific parameters from RABL config
            waveform_config: Dictionary containing base_frequency and breathing_amplitude
        """
        if shape_params is None:
            shape_params = {}
        
        if waveform_config is None:
            waveform_config = {
                'base_frequency': 1.0,
                'breathing_amplitude': 0.15,
                'line_width': 5
            }

        points = []
        start_index = len(normalized_data) // 2 - (self.width // 2)
        end_index = len(normalized_data) // 2 + (self.width // 2)

        # Time-varied amplitude for subtle breathing effect
        breathing_amplitude = waveform_config.get('breathing_amplitude', 0.15)
        time_amplitude_factor = 0.7 + breathing_amplitude * np.sin(current_time * 0.004)

        # Base frequency is normalized to screen width (1 cycle = full width)
        base_frequency = waveform_config.get('base_frequency', 1.0)

        if shape == "parabolic":
            # Parabolic shape with sine undulation - all points same Y at center
            parabolic_sine_frequency = shape_params.get('parabolic_sine_frequency', 0.05)
            parabolic_sine_amplitude = shape_params.get('parabolic_sine_amplitude', 5)
            curve_factor_intensity = shape_params.get('curve_factor_intensity', 1.0)
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                
                # Parabolic curve (inverted parabola, peak at center)
                normalized_position = (i - (self.width // 2)) / (self.width // 2)  # -1 to 1
                curve_factor = (1 - normalized_position**2) * curve_factor_intensity
                
                # Sine undulation on top of parabolic curve
                sine_undulation = (parabolic_sine_amplitude * time_amplitude_factor * 
                                 np.sin(i * parabolic_sine_frequency * 2 * np.pi / self.width + 
                                       current_time * base_frequency * 0.005))
                
                # Y position: center + audio amplitude + parabolic curve + sine undulation
                y = self.y + y_offset + (sample * amplitude_multiplier) + (curve_factor * 20) + sine_undulation
                points.append((x, y))

        elif shape == "saw":
            # Sawtooth wave - middle point at center Y
            saw_period_divisor = shape_params.get('saw_period_divisor', 8)
            base_saw_amplitude = shape_params.get('base_amplitude', 20)
            saw_frequency = shape_params.get('saw_frequency', 0.02)
            
            saw_period = self.width // saw_period_divisor
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                
                # Time-based sawtooth oscillation
                pos_in_cycle = (i + int(current_time * base_frequency * saw_frequency * 100)) % saw_period
                
                # Sawtooth triangle wave (goes up then down)
                if pos_in_cycle < saw_period / 2:
                    saw_offset = (pos_in_cycle / (saw_period / 2)) * (base_saw_amplitude + 40 * time_amplitude_factor)
                else:
                    saw_offset = ((saw_period - pos_in_cycle) / (saw_period / 2)) * (base_saw_amplitude + 40 * time_amplitude_factor)
                
                # Y position: center + audio amplitude + sawtooth offset
                y = self.y + y_offset + (sample * amplitude_multiplier) + saw_offset
                points.append((x, y))

        elif shape == "sine":
            # Sine wave - all points same Y at center (sine oscillates around center)
            sine_frequency = shape_params.get('sine_frequency', 0.015)
            sine_amplitude = shape_params.get('sine_amplitude', 10)
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                
                # Pure sine wave with base frequency
                sine_offset = (sine_amplitude * time_amplitude_factor * 
                             (1 + np.sin(i * sine_frequency * 2 * np.pi / self.width + 
                                        current_time * base_frequency * 0.01)))
                
                # Y position: center + audio amplitude + sine oscillation
                y = self.y + y_offset + (sample * amplitude_multiplier) + sine_offset
                points.append((x, y))

        else:  # Default
            # Simple line following audio amplitude
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                y = self.y + y_offset + (sample * amplitude_multiplier)
                points.append((x, y))

        # Clamp amplitude to prevent overlap with eyes
        if max_amplitude is not None:
            final_points = []
            for x, y in points:
                clamped_y = np.clip(y, self.y - max_amplitude, self.y + max_amplitude)
                final_points.append((x, int(clamped_y)))
            points = final_points

        # Draw the waveform
        if len(points) > 1:
            line_width = waveform_config.get('line_width', 5)
            pygame.draw.lines(screen, self.color, False, points, line_width)
