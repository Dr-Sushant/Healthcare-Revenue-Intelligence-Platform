"""
DRG analytics and revenue intelligence metrics.
"""

import pandas as pd


class DRGAnalytics:
    """
    Analytics methods for DRG-level insights.
    """

    def top_revenue_drgs(
        self,
        df: pd.DataFrame,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            df.groupby(
                ["DRG_Cd", "DRG_Desc"],
                as_index=False,
            )["Total_Revenue"]
            .sum()
            .sort_values(
                "Total_Revenue",
                ascending=False,
            )
            .head(top_n)
        )

    def top_volume_drgs(
        self,
        df: pd.DataFrame,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            df.groupby(
                ["DRG_Cd", "DRG_Desc"],
                as_index=False,
            )["Tot_Dschrgs"]
            .sum()
            .sort_values(
                by="Tot_Dschrgs",
                ascending=False,
            )
            .head(top_n)
        )

    def highest_revenue_per_discharge(
        self,
        df: pd.DataFrame,
        top_n: int = 10,
    ) -> pd.DataFrame:

        analytics_df = df.groupby(
            ["DRG_Cd", "DRG_Desc"],
            as_index=False,
        ).agg(
            Total_Revenue=("Total_Revenue", "sum"),
            Total_Discharges=("Tot_Dschrgs", "sum"),
        )

        analytics_df["Revenue_Per_Discharge"] = (
            analytics_df["Total_Revenue"] / analytics_df["Total_Discharges"]
        )

        return analytics_df.sort_values(
            by="Revenue_Per_Discharge",
            ascending=False,
        ).head(top_n)

    def highest_payment_variation_drgs(
        self,
        df: pd.DataFrame,
        top_n: int = 10,
    ) -> pd.DataFrame:

        analytics_df = df.groupby(
            ["DRG_Cd", "DRG_Desc"],
            as_index=False,
        )["Payment_Variation_Index"].mean()

        return analytics_df.sort_values(
            by="Payment_Variation_Index",
            ascending=False,
        ).head(top_n)

    def longest_los_drgs(
        self,
        df: pd.DataFrame,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            df[
                [
                    "DRG_Cd",
                    "DRG_Desc",
                    "Geometric mean LOS",
                ]
            ]
            .drop_duplicates()
            .sort_values(
                by="Geometric mean LOS",
                ascending=False,
            )
            .head(top_n)
        )
