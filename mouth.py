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
             current_time=0, max_amplitude=None, shape_params=None, waveform_config=None, cycle_rate=1.0):
        """
        Draw the mouth based on audio data.
        
        Args:
            screen: Pygame screen surface
            normalized_data: Normalized audio data array (from -1 to 1)
            y_offset: Vertical offset for the mouth shape
            amplitude_multiplier: Audio amplitude multiplier (0-100, where 0 = straight line)
                                Controls how much of the audio waveform affects the mouth
            shape: Shape type ('default', 'parabolic', 'sine', or 'saw')
            current_time: Current time in milliseconds (from pygame.time.get_ticks())
            max_amplitude: The maximum vertical distance the waveform can travel from center.
                          Prevents overlap with eyes (10% below eye position)
            shape_params: Dictionary of shape-specific parameters from RABL config
                         Frequency values: in terms of π (e.g., 2 = 2π radians)
            waveform_config: Dictionary containing base_frequency and breathing_amplitude
            cycle_rate: Animation cycle rate multiplier (1.0 = normal, 2.0 = double speed)
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

        # Normalize amplitude_multiplier from 0-100 scale to actual amplitude
        # amplitude_multiplier=0 results in straight line (no audio effect)
        # amplitude_multiplier=100 uses full normalized_data range (-1 to 1)
        normalized_amplitude = (amplitude_multiplier / 100.0) if amplitude_multiplier > 0 else 0.0
        
        # Time-varied amplitude for subtle breathing effect
        breathing_amplitude = waveform_config.get('breathing_amplitude', 0.15)
        time_amplitude_factor = 0.7 + breathing_amplitude * np.sin(current_time * 0.004)

        # Default base frequency in Hz (affects time-based animation speed)
        base_frequency = waveform_config.get('base_frequency', 1.0)

        if shape == "parabolic":
            # Parabolic shape with sine undulation
            # Frequency is specified in terms of π in config (e.g., 2 = 2π radians)
            parabolic_frequency_pi = shape_params.get('parabolic_sine_frequency', 2.0)
            parabolic_frequency = parabolic_frequency_pi * np.pi  # Convert from π terms to radians
            curve_direction = shape_params.get('curve_direction', 1.0)  # 1.0 for convex (smile), -1.0 for concave (frown)
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                
                # Parabolic curve (inverted parabola, peak at center by default)
                # curve_factor ranges from 0 at edges to 1 at center
                normalized_position = (i - (self.width // 2)) / (self.width // 2)  # -1 to 1
                curve_factor = (1 - normalized_position**2) * curve_direction
                
                # Sine undulation on top of audio and parabolic curve
                # Frequency parameter controls wave speed (higher = faster)
                # cycle_rate multiplier affects animation speed
                sine_undulation = (np.sin(i * parabolic_frequency / self.width + 
                                         current_time * base_frequency * cycle_rate * 0.005) * 
                                  time_amplitude_factor * 30)
                
                # Y position: center + audio amplitude + sine undulation + parabolic curve lift
                # Audio amplitude scaled by normalized_amplitude (0-1)
                y = (self.y + y_offset + 
                     (sample * normalized_amplitude * 50) +  # Scale audio by normalized_amplitude
                     sine_undulation +  # Sine wave motion
                     (curve_factor * 15))  # Subtle parabolic curve
                points.append((x, y))

        elif shape == "saw":
            # Sawtooth/triangle wave - oscillates around center Y
            # Frequency is specified in terms of π in config (e.g., 2 = 2π radians)
            saw_frequency_pi = shape_params.get('saw_frequency', 2.0)
            saw_frequency = saw_frequency_pi * np.pi  # Convert from π terms to radians
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                
                # Time-based sawtooth oscillation using frequency
                # Higher saw_frequency = faster oscillation
                # cycle_rate multiplier affects animation speed
                phase = (i * saw_frequency / self.width + current_time * base_frequency * cycle_rate * 0.01) % (2 * np.pi)
                
                # Triangle wave: goes from -1 to 1 and back
                # phase normalized to 0-2π
                if phase < np.pi:
                    triangle_offset = (phase / np.pi) * 60 - 30  # -30 to 30
                else:
                    triangle_offset = ((2 * np.pi - phase) / np.pi) * 60 - 30  # 30 to -30
                
                # Y position: center + audio amplitude + triangle offset
                # Using same amplitude as sine and parabolic for consistency
                y = (self.y + y_offset + 
                     (sample * normalized_amplitude * 50) +  # Scale audio by normalized_amplitude
                     (triangle_offset * time_amplitude_factor))
                points.append((x, y))

        elif shape == "sine":
            # Sine wave - oscillates around center Y
            # Frequency is specified in terms of π in config (e.g., 2 = 2π radians)
            sine_frequency_pi = shape_params.get('sine_frequency', 2.0)
            sine_frequency = sine_frequency_pi * np.pi  # Convert from π terms to radians
            
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                
                # Time-based sine oscillation using frequency
                # Higher sine_frequency = faster oscillation
                # cycle_rate multiplier affects animation speed
                phase = i * sine_frequency / self.width + current_time * base_frequency * cycle_rate * 0.005
                
                # Sine wave oscillation: -1 to 1 range, scaled to match sawtooth/parabolic
                sine_offset = np.sin(phase) * time_amplitude_factor * 30
                
                # Y position: center + audio amplitude + sine offset
                y = (self.y + y_offset + 
                     (sample * normalized_amplitude * 50) +  # Scale audio by normalized_amplitude
                     sine_offset)
                points.append((x, y))

        else:  # Default
            # Simple line following audio amplitude with normalized scaling
            for i, sample in enumerate(normalized_data[start_index:end_index]):
                x = int(self.x - (self.width // 2) + (i / self.width * self.width))
                # Audio amplitude scaled by normalized_amplitude (0-100 scale)
                y = self.y + y_offset + (sample * normalized_amplitude * 50)
                points.append((x, y))

        # Clamp amplitude to prevent overlap with eyes
        if max_amplitude is not None:
            final_points = []
            for x, y in points:
                # Use normalized_amplitude to scale the max_amplitude clamping
                clamp_range = max_amplitude * (normalized_amplitude if normalized_amplitude > 0 else 0.5)
                clamped_y = np.clip(y, self.y - clamp_range, self.y + clamp_range)
                final_points.append((x, int(clamped_y)))
            points = final_points

        # Draw the waveform
        if len(points) > 1:
            line_width = waveform_config.get('line_width', 5)
            pygame.draw.lines(screen, self.color, False, points, line_width)
