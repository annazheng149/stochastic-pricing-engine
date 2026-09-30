import asyncio
import pandas as pd

from src.models import MarketTick


def load_market_data(file_path: str) -> list[MarketTick]:
    df = pd.read_csv(file_path)

    ticks = []

    for _, row in df.iterrows():
        tick = MarketTick(
            timestamp=row["timestamp"],
            symbol=row["symbol"],
            price=row["price"],
            volume=row["volume"]
        )

        ticks.append(tick)

    return ticks


async def stream_market_data(ticks: list[MarketTick], delay: float = 1.0):
    for tick in ticks:
        yield tick
        await asyncio.sleep(delay)