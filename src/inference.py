import time
import logging
from models import Classifier
from globals import X_COLUMNS
from utils import load_yaml_config, fancy_print

# LOGGING
model_logger = logging.getLogger('model_logger')
model_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('model_logs.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
model_logger.addHandler(file_handler)

CONFIG_FILEPATH = "config.yaml"


class InferenceEngine:
    """
    Uses the specified classifier model to predict Valorant agent based on 
    user input.
    """

    def __init__(self) -> None:
        """Initialises user input."""
        self.input = {
            'Agent_Type': None,
            'Playstyle': None,
            'Difficulty': None,
            'Ability_Preference': None,
            'Gun_Type': None
        }
        self.config = load_yaml_config(CONFIG_FILEPATH)['inference']
        model_logger.info(f"Config file {CONFIG_FILEPATH} loaded successfully")
        self.classifier = Classifier(self.config['model_path'])
        model_logger.info(f"Classifier {self.config['model_path']} loaded successfully")
        print("Classifier loaded successfully")

    def get_user_input(self) -> None:
        """Stores the users inputs to be used for model inference."""
        for column in self.input:
            model_logger.info(f"Storing {column} value...")
            print()
            while True:
                try:
                    for count, option in enumerate(X_COLUMNS[column]):
                        print(f"{count+1}. {option}")
                    choice = int(input(f"\nChoose your {column}: ")) - 1
                    if choice in range (0, len(X_COLUMNS[column])):
                        break
                    print(f"Please enter a number between 1 and {len(X_COLUMNS[column])} only: ")
                except ValueError:
                    print(f"Please enter a valid number between 1 and {len(X_COLUMNS[column])} only: ")
            self.input[column] = X_COLUMNS[column][choice]

    def get_prediction(self) -> str:
        """Runs inference on the users inputs and returns the most suitable agent."""
        return self.classifier.run_inference(self.input)


if __name__ == '__main__':
    try:
        start_time = time.time()
        fancy_print("Valorant Agent Picker")
        inference_engine = InferenceEngine()
        inference_engine.get_user_input()
        model_logger.info("Performing inference..")
        agent = inference_engine.get_prediction()
        print(f"\n\nYour ideal Valorant agent is {agent}!\n\n")
        model_logger.info(f"Input was processed in {time.time() - start_time} seconds")
        fancy_print("The End")
    except Exception as e:
        print(f"An unexpected error occured: {str(e)}!")