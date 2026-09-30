import asyncio

from src.stream import load_market_data, stream_market_data


async def main():
    ticks = load_market_data("data/market_ticks.csv")

    print("Starting market data stream...\n")

    async for tick in stream_market_data(ticks, delay=1.0):
        print(
            f"{tick.timestamp} | "
            f"{tick.symbol} | "
            f"Price: ${tick.price:.2f} | "
            f"Volume: {tick.volume}"
        )


if __name__ == "__main__":
    asyncio.run(main())