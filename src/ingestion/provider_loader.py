"""
Provider data loader for Medicare inpatient utilization data.
"""

from pathlib import Path

import pandas as pd


SUPPORTED_ENCODINGS = [
    "utf-8",
    "latin1",
    "iso-8859-1",
    "cp1252",
]

PROVIDER_COLUMNS = [
    "DRG_Cd",
    "DRG_Desc",
    "Tot_Dschrgs",
]


class ProviderLoader:
    """
    Loads and validates Medicare provider data.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        """
        Load provider dataset and return cleaned dataframe.
        """
        for encoding in SUPPORTED_ENCODINGS:
            try:
                return pd.read_csv(
                    self.file_path,
                    usecols=PROVIDER_COLUMNS,
                    encoding=encoding,
                    low_memory=False,
                )
            except Exception as e:
                print(f"Encoding {encoding} failed: {e}")
                continue

        raise ValueError(
            f"Unable to read provider file: {self.file_path}"
        )