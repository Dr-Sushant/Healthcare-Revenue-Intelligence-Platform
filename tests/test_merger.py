from src.ingestion.provider_loader import ProviderLoader
from src.ingestion.ipps_loader import IPPSLoader
from src.transform.merger import DRGMerger

provider_df = ProviderLoader(
    "data/Medicare_IP_Hospitals_by_Provider_and_Service_2024.csv"
).load()

ipps_df = IPPSLoader(
    "data/CMS-1833-F Table 5.xlsx"
).load()

merged_df = DRGMerger().merge(
    provider_df,
    ipps_df,
)

print(merged_df.head())
print()
print(merged_df.shape)
print()
print(merged_df.columns.tolist())