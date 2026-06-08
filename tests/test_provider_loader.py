from src.ingestion.provider_loader import ProviderLoader


loader = ProviderLoader(
    "data/Medicare_IP_Hospitals_by_Provider_and_Service_2024.csv"
)

df = loader.load()

print(df.head())
print(df.shape)
print(df.columns.tolist())