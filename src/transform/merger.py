"""
Merge provider and IPPS datasets.
"""

import pandas as pd


class DRGMerger:
    """
    Merge Medicare provider data with IPPS reference data.
    """

    def merge(
        self,
        provider_df: pd.DataFrame,
        ipps_df: pd.DataFrame,
    ) -> pd.DataFrame:
        return pd.merge(
            provider_df,
            ipps_df,
            left_on="DRG_Cd",
            right_on="MS-DRG",
            how="inner",
        )