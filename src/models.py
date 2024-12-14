import pandas as pd
import torch
from llama_cpp import Llama
import pickle
from globals import PREPROCESSED_X_COLUMNS, DIFFICULTY_MAPPINGS, AGENT_MAPPINGS


class GGUFModel:
    """Handles the GGUF model being used for dataset_preparation_automatic."""

    def __init__(self, parameters: dict) -> None:
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
    
    def perform_inference(self, input: dict) -> str:
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


class Classifier:
    """Handles the classification model."""

    def __init__(self, model_path: str) -> None:
        """Loads the classifier."""
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)

    def get_preprocessed_input(self, input_dict: dict) -> pd.DataFrame:
        """
        Applies the preprocessing/encodings that were used on the dataset during 
        model training.
        """
        example_data_preprocessed = pd.DataFrame([[''] * len(PREPROCESSED_X_COLUMNS)], columns=PREPROCESSED_X_COLUMNS)
        example_data_columns = PREPROCESSED_X_COLUMNS[:]
        for column in example_data_columns:
            for current_column, current_column_value in input_dict.items():
                if current_column in column:
                    # ORDINAL COLUMNS
                    if current_column == 'Difficulty':
                        example_data_preprocessed[column] = DIFFICULTY_MAPPINGS[input_dict['Difficulty']]
                    # ONE HOT ENCODING COLUMNS
                    else:
                        if current_column_value in column:
                            example_data_preprocessed[column] = True
                        else:
                            example_data_preprocessed[column] = False
        return example_data_preprocessed

    def run_inference(self, input_dict: dict) -> str:
        """ Predicts the Valorant Agent that is most suitable for the given input"""
        preprocessed_input = self.get_preprocessed_input(input_dict)
        example_data_pred = self.model.predict(preprocessed_input)
        agent = AGENT_MAPPINGS[example_data_pred[0]]
        return agent

