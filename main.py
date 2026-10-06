import asyncio

from src.stream import load_market_data, stream_market_data
from src.analytics import MarketAnalytics


async def main():
    ticks = load_market_data("data/market_ticks.csv")

    analytics = MarketAnalytics(window_size=100)

    print("Starting market data stream...\n")

    async for tick in stream_market_data(ticks, delay=1.0):
        
        analytics.add_price(tick.price)
        volatility = analytics.calculate_volatility()
        
        print(
            f"{tick.timestamp} | "
            f"{tick.symbol} | "
            f"Price: ${tick.price:.2f} | "
            f"Volume: {tick.volume} | "
            f"Volatility: {volatility:6f}"
        )


if __name__ == "__main__":
    asyncio.run(main())