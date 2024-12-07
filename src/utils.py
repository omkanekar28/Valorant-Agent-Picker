from typing import Dict, Any
import yaml
import pyfiglet

def fancy_print(text: str):
    """Use this for starting and ending prints."""
    ascii_art = pyfiglet.figlet_format(text)
    print(ascii_art)

def load_yaml_config(yaml_file_path: str) -> Dict[str, Any]:
    """Loads the configuration settings from a YAML file."""
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
