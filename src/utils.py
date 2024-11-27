from typing import Dict, Any
import yaml

def load_config(yaml_file_path: str) -> Dict[str, Any]:
    """Loads the configuration settings from a YAML file."""
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
