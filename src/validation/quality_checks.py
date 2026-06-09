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

    def unmapped_drg_codes(
        self,
        provider_df: pd.DataFrame,
        merged_df: pd.DataFrame,
    ) -> pd.DataFrame:

        mapped_drgs = set(merged_df["DRG_Cd"])

        return (
            provider_df[~provider_df["DRG_Cd"].isin(mapped_drgs)]
            .groupby(
                ["DRG_Cd", "DRG_Desc"],
                as_index=False,
            )
            .size()
            .sort_values(
                "size",
                ascending=False,
            )
        )

    def unmapped_drg_summary(
        self,
        provider_df: pd.DataFrame,
        merged_df: pd.DataFrame,
    ) -> pd.DataFrame:

        unmapped_df = self.unmapped_drg_codes(
            provider_df,
            merged_df,
        ).copy()

        unmapped_df["Percent_of_Unmapped"] = round(
            (unmapped_df["size"] / unmapped_df["size"].sum()) * 100,
            2,
        )

        return unmapped_df

    def deprecated_drg_report(
        self,
        provider_df: pd.DataFrame,
        merged_df: pd.DataFrame,
    ) -> pd.DataFrame:

        report = self.unmapped_drg_summary(
            provider_df,
            merged_df,
        ).copy()

        report["Potential_Status"] = "Absent from FY2026 IPPS"

        return report
