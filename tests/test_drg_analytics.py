from src.ingestion.provider_loader import ProviderLoader
from src.ingestion.ipps_loader import IPPSLoader
from src.transform.merger import DRGMerger
from src.transform.revenue_metrics import RevenueMetrics
from src.analytics.drg_analytics import DRGAnalytics

provider_df = ProviderLoader(
    "data/Medicare_IP_Hospitals_by_Provider_and_Service_2024.csv"
).load()

ipps_df = IPPSLoader("data/CMS-1833-F Table 5.xlsx").load()

merged_df = DRGMerger().merge(
    provider_df,
    ipps_df,
)

final_df = RevenueMetrics().add_metrics(merged_df)

analytics = DRGAnalytics()

print("\nTop Revenue DRGs:")

print(analytics.top_revenue_drgs(final_df).to_string(index=False))

print("\nTop Volume DRGs:")

print(analytics.top_volume_drgs(final_df).to_string(index=False))

print("\nHighest Revenue Per Discharge:")

print(analytics.highest_revenue_per_discharge(final_df).to_string(index=False))

print("\nLongest LOS DRGs:")

print(analytics.longest_los_drgs(final_df).to_string(index=False))
