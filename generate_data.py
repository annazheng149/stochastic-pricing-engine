import numpy as np
import pandas as pd

np.random.seed(42)

number_of_ticks = 1000
starting_price = 254.00

timestamps = pd.date_range(
    start="2026-9-29 09:30:00",
    periods = number_of_ticks,
    freq="s"
)

returns = np.random.normal(
    loc=0,
    scale=0.0003,
    size=number_of_ticks
)

prices = starting_price * np.exp(np.cumsum(returns))

volumes = np.random.randint(
    50,
    1000,
    size=number_of_ticks
)

data = pd.DataFrame({
    "timestamp": timestamps,
    "symbol": "APPL",
    "price": prices,
    "volume": volumes
})

data["price"] = data["price"].round(2)

data.to_csv(
    "data/market_ticks.csv",
    index=False
)

print("Generated 1,000 market tickets.")