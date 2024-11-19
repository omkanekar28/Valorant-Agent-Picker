import os
import itertools
import config
import pandas as pd


class DataHandler:
    """Class that maintains the data and relevant operations."""

    def __init__(self) -> None:
        """Initialises the data."""
        self.columns = list(config.COLUMNS.keys())
        self.column_values_list = list(config.COLUMNS.values())
        self.data = pd.DataFrame(columns=self.columns)

    def generate_rows(self) -> None:
        """Creates each possible unique entry in the dataset."""
        rows = list(itertools.product(*self.column_values_list))    # GENERATE ALL POSSIBLE COMBINATIONS OF VALUES FOR EACH COLUMN USING 'itertools.product'
        self.data = pd.DataFrame(rows, columns=self.columns)

    def save_dataset(self, save_dir: str) -> None:
        """Saves the dataset in specified directory."""
        self.data.to_excel(os.path.join(save_dir, "dataset.xlsx"))


if __name__ == '__main__':
    data_handler = DataHandler()
    data_handler.generate_rows()
    data_handler.save_dataset(config.DATASET_SAVE_DIR)
