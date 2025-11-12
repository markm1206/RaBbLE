import yaml
import os

def parse_rabl(file_path):
    """
    Parses a .rabl file (YAML-like structure) into a Python dictionary using PyYAML.
    
    Args:
        file_path: Path to the RABL file. Can be relative or absolute.
                  If relative, will be resolved relative to the script's directory.
    
    Returns:
        Dictionary containing parsed RABL data, or None if parsing fails.
    """
    try:
        # If the path is relative, resolve it relative to this script's directory
        if not os.path.isabs(file_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, file_path)
        
        # Expand user home directory if needed
        file_path = os.path.expanduser(file_path)
        
        # Normalize the path
        file_path = os.path.normpath(file_path)
        
        print(f"Loading RABL configuration from: {file_path}")
        
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        print(f"Successfully loaded RABL configuration.")
        return data
    except FileNotFoundError:
        print(f"Error: RABL file not found at {file_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing RABL file {file_path}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error loading RABL file: {e}")
        return None

if __name__ == '__main__':
    # Example Usage and Test
    example_rabl_content = """
# This is a comment
emotion_config:
  IDLE:
    blink_interval: 1000
    mouth_shape: sine
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      sine_frequency: 0.05
      sine_amplitude: 10
  HAPPY:
    blink_interval: 1000
    mouth_shape: parabolic
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      parabolic_sine_frequency: 0.03
      parabolic_sine_amplitude: 5
  SAD:
    blink_interval: 2000
    mouth_shape: parabolic
    y_offset: 0
    amplitude_multiplier: 600
    shape_params:
      parabolic_sine_frequency: 0.03
      parabolic_sine_amplitude: 5
  ANGRY:
    blink_interval: 500
    mouth_shape: saw
    y_offset: 0
    amplitude_multiplier: 700
    shape_params:
      saw_period_divisor: 8
      base_amplitude: 20
"""
    test_file_path = "test_emotions.rabl"
    with open(test_file_path, "w") as f:
        f.write(example_rabl_content)

    parsed_data = parse_rabl(test_file_path)
    print("Parsed RABL Data:")
    print(parsed_data)

    # Clean up test file
    os.remove(test_file_path)
