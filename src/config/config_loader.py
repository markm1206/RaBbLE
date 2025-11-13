import os
import yaml

class ConfigLoader:
    def __init__(self, config_dir="config"):
        self.config_dir = config_dir
        self.config = {}

    def load_config(self):
        """
        Loads all .rabl files from the config directory and merges them into a single dictionary.
        """
        config_path = os.path.join(os.path.dirname(__file__), '..', '..', self.config_dir)
        
        for filename in os.listdir(config_path):
            if filename.endswith(".rabl"):
                file_path = os.path.join(config_path, filename)
                try:
                    with open(file_path, 'r') as f:
                        # Use SafeLoader to prevent arbitrary code execution
                        self.config.update(yaml.safe_load(f))
                except FileNotFoundError:
                    print(f"Error: Configuration file not found at {file_path}")
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML in {file_path}: {e}")
        return self.config

    def get(self, key, default=None):
        """
        Retrieves a configuration value using a dot-separated key (e.g., 'display_config.width').
        """
        keys = key.split('.')
        val = self.config
        try:
            for k in keys:
                val = val[k]
            return val
        except KeyError:
            return default

    def print_config(self, indent=0):
        """
        Prints the loaded configuration in a well-formatted, indented manner.
        """
        def _print_dict(d, current_indent):
            for key, value in d.items():
                print(f"{'  ' * current_indent}{key}:", end="")
                if isinstance(value, dict):
                    print()
                    _print_dict(value, current_indent + 1)
                elif isinstance(value, list):
                    print()
                    for item in value:
                        print(f"{'  ' * (current_indent + 1)}- {item}")
                else:
                    print(f" {value}")
        
        print(f"{'  ' * indent}Configuration:")
        _print_dict(self.config, indent + 1)
