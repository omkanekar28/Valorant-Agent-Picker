import os
import itertools
import pandas as pd
from utils import load_config

CONFIG_FILEPATH = "/home/om/code/Valorant-Agent-Picker/src/config.yaml"


class DatasetInitializer:
    """Handles dataset creation and saving operations."""

    def __init__(self) -> None:
        """Initializes the dataset with configuration and column definitions."""
        self.config = load_config(CONFIG_FILEPATH)["dataset_initialization"]
        self.columns = {
            "Agent_Type": ["Duelist", "Initiator", "Controller", "Sentinel"],
            "Playstyle": ["Balanced", "Aggressive", "Supportive", "Map-control", "Info-gathering"],
            "Difficulty": ["Easy", "Hard"],
            "Ability_Preference": ["Flashes", "Smokes", "Healing", "Agility", "Information"],
            "Gun_Type": ["SMGs", "Shotguns", "Rifles", "Snipers", "Machine Guns"]
        }
        self.data = pd.DataFrame(columns=self.columns)
        self.save_dir = self.config["dataset_store_dir"]

    def generate_rows(self) -> None:
        """Generates all possible combinations of column values and creates a DataFrame."""
        column_values_list = [column_value for column_value in self.columns.values()]
        rows = list(itertools.product(*column_values_list))    # GENERATE ALL POSSIBLE COMBINATIONS OF VALUES FOR EACH COLUMN USING 'itertools.product'
        self.data = pd.DataFrame(rows, columns=self.columns.keys())
        self.data['Agent'] = None

    def save_dataset(self) -> None:
        """Saves the generated dataset to an Excel file in the specified directory."""
        self.data.to_excel(os.path.join(self.save_dir, "dataset_incomplete.xlsx"))


if __name__ == '__main__':
    dataset_initializer = DatasetInitializer()
    dataset_initializer.generate_rows()
    dataset_initializer.save_dataset()
