import pandas as pd
from data_fetcher import COTFetcher
from analyzer import COTAnalyzer

print("Fetching data...")
fetcher = COTFetcher()
df = fetcher.fetch_recent_data('traders_in_financial_futures_fut')
print(f"Dataframe shape: {df.shape}")

if df is not None and not df.empty:
    analyzer = COTAnalyzer(df)
    assets = analyzer.get_assets()
    print(f"Found {len(assets)} assets:")
    print(assets[:10])
else:
    print("DataFrame is empty or None!")
