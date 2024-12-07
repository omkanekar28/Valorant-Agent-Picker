from models import Classifier
from globals import X_COLUMNS
from utils import load_yaml_config, fancy_print

CONFIG_FILEPATH = "/home/om/code/Valorant-Agent-Picker/src/config.yaml"


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
        self.classifier = Classifier(self.config['model_path'])

    def get_user_input(self) -> None:
        """Stores the users inputs to be used for model inference."""
        for column in self.input:
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
    fancy_print("Valorant Agent Picker")
    inference_engine = InferenceEngine()
    inference_engine.get_user_input()
    agent = inference_engine.get_prediction()
    print(f"\n\nYour ideal Valorant agent is {agent}!\n\n")
    fancy_print("The End")