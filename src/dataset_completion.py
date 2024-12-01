import os
import pandas as pd
from utils import GGUFModelHandler, load_config

CONFIG_FILEPATH = "/home/om/code/Valorant-Agent-Picker/src/config.yaml"


class DatasetCompleter:
    """Handles dataset completion and saving operations."""
    
    def __init__(self) -> None:
        """Initialises the parameters needed for dataset completion."""
        self.config = load_config(CONFIG_FILEPATH)['dataset_completion']
        self.model_handler = GGUFModelHandler(self.config['model'])
        self.dataset = pd.read_excel(self.config['dataset']['path'])
        self.store_dir = self.config['misc']['store_dir']
        self.agents = {
            'Brimstone', 'Phoenix', 'Sage', 'Sova', 'Viper', 'Cypher', 'Reyna', 'Killjoy', 'Breach', 'Omen', 'Jett', 'Raze', 'Skye', 'Yoru', 'Astra', 'Kayo', 'Chamber', 'Neon', 'Fade', 'Harbor', 'Gekko', 'Deadlock', 'Iso', 'Clove', 'Vyse'
        }

    def fill_rows(self) -> None:
        """Uses the specified model to predict the agent name, validates the output and 
        stores in a new excel file."""
        self.dataset['Agent'] = self.dataset['Agent'].astype('object')
        for index, row in self.dataset.iterrows():
            try:
                print(f"Processing row {index+1} out of {self.dataset.shape[0]}")
                model_input = f"Agent Type: {row['Agent_Type']}, Playstyle: {row['Playstyle']}, Difficulty: {row['Difficulty']}, Team Dependent: {row['Team_Dependent']}, Ability Preference: {row['Ability_Preference']}, Gun Type: {row['Gun_Type']}"
                predicted_agent_name = self.model_handler.perform_inference(model_input)
                number_of_tries = 0

                # IF NOT CORRECT PREDICTION, TRY AGAIN TILL LIMIT IS HIT
                while number_of_tries < self.config['misc']['max_number_of_tries']:
                    predicted_agent_name = predicted_agent_name.title()
                    if predicted_agent_name in self.agents:
                        break
                    number_of_tries += 1
                
                print(model_input)
                print(predicted_agent_name)
                print()

                # IF MODEL FAILS TO PREDICT CORRECT OUTPUT
                if number_of_tries == self.config['misc']['max_number_of_tries']:
                    self.dataset.at[index, 'Agent'] = 'Not Found'
                # IF MODEL PREDICTS SUCCESSFULLY
                else:
                    self.dataset.at[index, 'Agent'] = predicted_agent_name
            except Exception as e:
                print(f"Skipping row {index+1}: {str(e)}")
                self.dataset.at[index, 'Agent'] = 'Not Found'
                continue
            finally:
                self.dataset.to_excel(os.path.join(self.store_dir, 'dataset_complete.xlsx'), index=False)


if __name__ == '__main__':
    dataset_completer = DatasetCompleter()
    dataset_completer.fill_rows()