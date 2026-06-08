"""
Revenue metric calculations.
"""

import pandas as pd


class RevenueMetrics:
    """
    Calculate revenue intelligence metrics.
    """

    def add_metrics(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        
        df = df.copy()

        df["Total_Revenue"] = (
            df["Avg_Tot_Pymt_Amt"] *
            df["Tot_Dschrgs"]
        )

        df["Payment_Variation_Index"] = (
            df["Avg_Tot_Pymt_Amt"] /
            df["Avg_Mdcr_Pymt_Amt"]
        )

        return df