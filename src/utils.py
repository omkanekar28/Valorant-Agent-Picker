from typing import Dict, Any
import yaml
import pyfiglet
import torch
from llama_cpp import Llama


class GGUFModelHandler:
    """Handles the GGUF model being used for inference."""

    def __init__(self, parameters) -> None:
        """Initializes the model and its relevant parameters."""
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.system_prompt = parameters['system_prompt']
        self.instruction_prompt = parameters['instruction_prompt']
        self.model = Llama(
            model_path=parameters['path'],
            n_gpu_layers= -1 if self.device=='cuda' else 0,
            n_ctx=parameters['context_window_size'],
            verbose=False
        )
        if self.device == 'cuda':
            print("Model loaded successfully on GPU.\n")
        else:
            print("Model loaded successfully on CPU.\n")
    
    def perform_inference(self, input) -> str:
        """Performs inference on the given input and returns the model output."""
        messages = [
            {"role": "user", "content": self.instruction_prompt},
            {"role": "user", "content": input}
        ]
        if self.system_prompt is not None:
            messages.insert(0, {"role": "system", "content": self.system_prompt})
        output = self.model.create_chat_completion(
            messages=messages,
        )
        text = output['choices'][0]['message']['content']
        return text

def fancy_print(text):
    ascii_art = pyfiglet.figlet_format(text)
    print(ascii_art)

def load_config(yaml_file_path: str) -> Dict[str, Any]:
    """Loads the configuration settings from a YAML file."""
    with open(yaml_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
