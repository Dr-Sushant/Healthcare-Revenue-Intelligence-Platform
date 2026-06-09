from src.ingestion.provider_loader import ProviderLoader
from src.ingestion.ipps_loader import IPPSLoader
from src.transform.merger import DRGMerger
from src.transform.revenue_metrics import RevenueMetrics
from src.validation.quality_checks import QualityChecks

provider_df = ProviderLoader(
    "data/Medicare_IP_Hospitals_by_Provider_and_Service_2024.csv"
).load()

ipps_df = IPPSLoader("data/CMS-1833-F Table 5.xlsx").load()

merged_df = DRGMerger().merge(
    provider_df,
    ipps_df,
)

final_df = RevenueMetrics().add_metrics(merged_df)

quality_checks = QualityChecks()

summary = quality_checks.summarize(final_df)

print("Dataset Summary:")
print(summary)

print("\nProvider DRG dtype:")
print(provider_df["DRG_Cd"].dtype)

print("\nMerged DRG dtype:")
print(merged_df["DRG_Cd"].dtype)

print("\nUnmapped DRGs:")
print(
    quality_checks.unmapped_drg_count(
        provider_df,
        merged_df,
    )
)

print("\nUnmapped DRG Rate:")
print(
    quality_checks.unmapped_drg_rate(
        provider_df,
        merged_df,
    )
)

print("\nTop Unmapped DRGs:")

print(
    quality_checks.unmapped_drg_codes(
        provider_df,
        merged_df,
    ).to_string()
)

print("\nUnmapped DRG Summary:")

print(
    quality_checks.unmapped_drg_summary(
        provider_df,
        merged_df,
    ).to_string(index=False)
)
