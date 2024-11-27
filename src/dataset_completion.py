import pandas as pd
import torch
from llama_cpp import Llama
from utils import load_config

CONFIG_FILEPATH = "/home/om/code/Valorant-Agent-Picker/src/config.yaml"


class ModelHandler:
    """Handles the model being used to generate dataset outputs."""

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
            print("Model loaded successfully on GPU.")
        else:
            print("Model loaded successfully on CPU.")
    
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


class DatasetCompleter:
    """Handles dataset completion and saving operations."""
    
    def __init__(self):
        self.config = load_config(CONFIG_FILEPATH)['dataset_completion']
        self.model_handler = ModelHandler(self.config['model'])
        self.dataset = pd.read_excel(self.config['dataset']['path'])
    
    def fill_rows(self):
        for _, row in self.dataset.iterrows():
            model_input = f"Agent Type: {row['Agent_Type']}, Playstyle: {row['Playstyle']}, Difficulty: {row['Difficulty']}, Team Dependent: {row['Team_Dependent']}, Ability Preference: {row['Ability_Preference']}, Gun Type: {row['Gun_Type']}"
            print(self.model_handler.perform_inference(model_input))
            # TODO: Validate model output and store results in excel.

if __name__ == '__main__':
    dataset_completer = DatasetCompleter()
    dataset_completer.fill_rows()