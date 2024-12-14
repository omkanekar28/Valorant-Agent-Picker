import os
import itertools
import pandas as pd
from globals import X_COLUMNS
from utils import load_yaml_config

CONFIG_FILEPATH = "config.yaml"


class DatasetInitializer:
    """Handles dataset creation and saving operations."""

    def __init__(self) -> None:
        """Initializes the dataset with configuration and column definitions."""
        self.config = load_yaml_config(CONFIG_FILEPATH)["dataset_initialization"]
        self.data = pd.DataFrame(columns=X_COLUMNS)
        self.save_dir = self.config["dataset_store_dir"]

    def generate_rows(self) -> None:
        """Generates all possible combinations of column values and creates a DataFrame."""
        column_values_list = [column_value for column_value in X_COLUMNS.values()]
        rows = list(itertools.product(*column_values_list))    # GENERATE ALL POSSIBLE COMBINATIONS OF VALUES FOR EACH COLUMN USING 'itertools.product'
        self.data = pd.DataFrame(rows, columns=X_COLUMNS.keys())
        self.data['Agent'] = None

    def save_dataset(self) -> None:
        """Saves the generated dataset to an Excel file in the specified directory."""
        self.data.to_excel(os.path.join(self.save_dir, "dataset_incomplete.xlsx"), index=False)


if __name__ == '__main__':
    dataset_initializer = DatasetInitializer()
    dataset_initializer.generate_rows()
    dataset_initializer.save_dataset()
