"""
Data quality and governance checks.
"""

import pandas as pd


class QualityChecks:
    """
    Validation checks for the Revenue Intelligence dataset.
    """

    def summarize(
        self,
        df: pd.DataFrame,
    ) -> dict:

        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "null_cells": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
        }

    def unmapped_drg_count(
        self,
        provider_df: pd.DataFrame,
        merged_df: pd.DataFrame,
    ) -> int:

        mapped_drgs = set(merged_df["DRG_Cd"])

        return int((~provider_df["DRG_Cd"].isin(mapped_drgs)).sum())

    def unmapped_drg_rate(
        self,
        provider_df: pd.DataFrame,
        merged_df: pd.DataFrame,
    ) -> float:

        unmapped_count = self.unmapped_drg_count(
            provider_df,
            merged_df,
        )

        return round(
            (unmapped_count / len(provider_df)) * 100,
            2,
        )
