import yaml
import os

def parse_rabl(file_path):
    """
    Parses a .rabl file (YAML-like structure) into a Python dictionary using PyYAML.
    Also handles loading referenced config files (e.g., emotions_file reference).
    
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
        
        # Check if there's a reference to another config file (e.g., emotions_file)
        if isinstance(data, dict):
            config_dir = os.path.dirname(file_path)
            
            # Handle emotions_file reference
            if 'emotions_file' in data:
                emotions_file_path = os.path.join(config_dir, data['emotions_file'])
                emotions_file_path = os.path.normpath(emotions_file_path)
                
                print(f"Loading referenced emotions file from: {emotions_file_path}")
                
                with open(emotions_file_path, 'r') as f:
                    emotions_data = yaml.safe_load(f)
                
                # Merge emotion_config from the separate file
                if emotions_data and 'emotion_config' in emotions_data:
                    data['emotion_config'] = emotions_data['emotion_config']
                
                # Remove the reference key from the main data
                del data['emotions_file']
            
            # Handle transcription_file reference
            if 'transcription_file' in data:
                transcription_file_path = os.path.join(config_dir, data['transcription_file'])
                transcription_file_path = os.path.normpath(transcription_file_path)
                
                print(f"Loading referenced transcription file from: {transcription_file_path}")
                
                with open(transcription_file_path, 'r') as f:
                    transcription_data = yaml.safe_load(f)
                
                # Merge transcription_config from the separate file
                if transcription_data and 'transcription_config' in transcription_data:
                    data['transcription_config'] = transcription_data['transcription_config']
                
                # Remove the reference key from the main data
                del data['transcription_file']
        
        print(f"Successfully loaded RABL configuration.")
        return data
    except FileNotFoundError as e:
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
