import subprocess
import yaml
import pyfiglet
from typing import Dict, Any

def fancy_print(text: str):
    """Use this for starting and ending prints."""
    ascii_art = pyfiglet.figlet_format(text)
    print(ascii_art)

def load_yaml_config(yaml_file_path: str) -> Dict[str, Any]:
    """Loads the configuration settings from a YAML file."""
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def is_nvidia_gpu_available():
    try:
        result = subprocess.run(
            ["nvidia-smi", "-L"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0 and "GPU " in result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False