import yfinance as yf
import pandas as pd

SYMBOL = "AAPL"
PERIOD = "5d"
INTERVAL = "1m"

print(f"Downloading {SYMBOL} market data...")

data = yf.download(
    tickers=SYMBOL,
    period=PERIOD,
    interval=INTERVAL,
    auto_adjust=True,
    progress=False
)

if data.empty:
    raise RuntimeError("No market data was downloaded.")

#yfinance can return MultiIndex columns.
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

data = data.reset_index()

#Keep only hte fields our engine needs
data = data [[
    "Datetime",
    "Close",
    "Volume"
]]

data = data.rename(
    columns={
        "Datetime": "timestamp",
        "Close": "price",
        "Volume": "volume"
    }
)

data["symbol"] = SYMBOL

data = data[[
    "timestamp",
    "symbol",
    "price",
    "volume"
]]

data = data.dropna()

data["price"] = data["price"].round(2)
data["volume"] = data["volume"].astype(int)

data.to_csv(
    "data/market_ticks.csv",
    index=False
)

print(f"Saved {len(data)} real market observations.")
print()
print(data.head())