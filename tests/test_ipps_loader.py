from src.ingestion.ipps_loader import IPPSLoader

loader = IPPSLoader(
    "data/CMS-1833-F Table 5.xlsx"
)

df = loader.load()

print(df.head())
print(df.shape)
print(df.columns.tolist())