from src.ingestion.provider_loader import ProviderLoader
from src.ingestion.ipps_loader import IPPSLoader

provider_df = ProviderLoader(
    "data/Medicare_IP_Hospitals_by_Provider_and_Service_2024.csv"
).load()

ipps_df = IPPSLoader(
    "data/CMS-1833-F Table 5.xlsx"
).load()

print("Provider DRG dtype:")
print(provider_df["DRG_Cd"].dtype)

print("\nIPPS DRG dtype:")
print(ipps_df["MS-DRG"].dtype)