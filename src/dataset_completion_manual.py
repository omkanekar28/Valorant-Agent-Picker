import os
import pandas as pd
from utils import load_config, fancy_print

CONFIG_FILEPATH = "/home/om/code/Valorant-Agent-Picker/src/config.yaml"


class DatasetCompleterManual:
    """
    Facilitates manual dataset completion by enabling users to fill in the data efficiently 
    and conveniently, without relying on an automated model.
    """

    def __init__(self) -> None:
        """Initialises the parameters needed for dataset completion."""
        self.config = load_config(CONFIG_FILEPATH)['dataset_completion_manual']
        self.dataset_path = self.config['dataset']['path']
        self.dataset = pd.read_excel(self.dataset_path)
        self.header = ["Agent_Type", "Playstyle", "Difficulty", "Ability_Preference", "Gun_Type"]
        self.agents = ['Phoenix', 'Reyna', 'Jett', 'Raze', 'Yoru', 'Neon', 'Iso', 
                    'Sova', 'Breach', 'Skye', 'Fade', 'Gekko', 'Clove', 
                    'Brimstone', 'Viper', 'Omen', 'Astra', 'Harbor', 'Vyse', 
                    'Sage', 'Cypher', 'Killjoy', 'Chamber', 'Deadlock']
        self.column_widths = [15, 15, 12, 18, 20, 10]

    def fill_rows(self) -> None:
        """Iterates through each row prompting the user to enter agent name for that specific row."""
        self.dataset['Agent'] = self.dataset['Agent'].astype('object')
        for index, row in self.dataset.iterrows():
            try:
                print(f"Processing row {index+1} out of {self.dataset.shape[0]}\n")
                
                # SKIP TO THE FIRST ROW WHICH HAS NOT BEEN FILLED YET
                if not pd.isna(self.dataset.at[index, 'Agent']):
                    print(f"Skipping row {index+1} as it is already filled\n")
                    continue
                
                for count, agent in enumerate(self.agents):
                    print(f"{count+1}. {agent}")

                print()
                print(" | ".join([self.header[i].ljust(self.column_widths[i]) for i in range(len(self.header))]))
                print(" | ".join([
                    str(row['Agent_Type']).ljust(self.column_widths[0]),
                    str(row['Playstyle']).ljust(self.column_widths[1]),
                    str(row['Difficulty']).ljust(self.column_widths[2]),
                    str(row['Ability_Preference']).ljust(self.column_widths[3]),
                    str(row['Gun_Type']).ljust(self.column_widths[5]),
                ]))
                
                while True:
                    try:
                        predicted_agent_index = int(input("\nEnter your choice: ")) - 1
                        if predicted_agent_index in range (0, len(self.agents)):
                            break
                        print(f"Please enter a number between 1 and {len(self.agents)} only: ")
                    except ValueError:
                        print(f"Please enter a valid number between 1 and {len(self.agents)} only: ")

                predicted_agent_name = self.agents[predicted_agent_index]
                self.dataset.at[index, 'Agent'] = predicted_agent_name
                self.dataset.to_excel(self.dataset_path, index=False)
                print(f"\nAgent {predicted_agent_name} stored successfully for row {index+1}\n")
            except Exception as e:
                print(f"\nSkipping row {index+1}: {str(e)}\n")
                self.dataset.at[index, 'Agent'] = 'Not Found'
                self.dataset.to_excel(self.dataset_path, index=False)
                continue
        print("All the rows have been filled successfully! Renaming excel from dataset_incomplete.xlsx to dataset_complete.xlsx...")
        dataset_complete_filepath = os.path.join(os.path.dirname(self.dataset_path), "dataset_complete.xlsx")
        self.dataset.to_excel(dataset_complete_filepath, index=False)
        os.remove(self.dataset_path)

if __name__ == '__main__':
    fancy_print("Manual Dataset Completion")
    dataset_completer = DatasetCompleterManual()
    dataset_completer.fill_rows()
    fancy_print("The End")