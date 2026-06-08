"""
IPPS Table 5 loader.
"""

from pathlib import Path

import pandas as pd


IPPS_COLUMNS = [
    "MS-DRG",
    "MS-DRG Title",
    "Weights - Before Cap",
    "Geometric mean LOS",
]


class IPPSLoader:
    """
    Loads FY2026 IPPS Table 5 data.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        """
        Load IPPS dataset.
        """
        df = pd.read_excel(
            self.file_path,
            skiprows=1
        )

        df.columns = [str(col).strip() for col in df.columns]

        return df[IPPS_COLUMNS].copy()