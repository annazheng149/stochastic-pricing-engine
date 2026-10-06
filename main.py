import asyncio

from src.stream import load_market_data, stream_market_data
from src.analytics import MarketAnalytics
from src.simulation import MonteCarloSimulator


async def main():
    ticks = load_market_data("data/market_ticks.csv")

    analytics = MarketAnalytics(window_size=100)

    simulator = MonteCarloSimulator(num_simulations=10_000, num_steps=60)

    print("Starting market data stream...\n")

    async for tick in stream_market_data(ticks, delay=0.5):
        
        analytics.add_price(tick.price)

        #Wait until there is enough market history
        if len(analytics.prices) < 20:
            print(
                f"{tick.symbol} | "
                f"${tick.price:.2f} | "
                f"Collecting market data..."
            )

            continue 

        volatility = analytics.calculate_volatility()
        drift = analytics.calculate_drift()

        path = simulator.simulate(
            current_price=tick.price,
            drift=drift,
            volatility=volatility
        )

        results = simulator.summarize(path)
        
        print(
            f"{tick.symbol} | "
            f"Current: ${tick.price:.2f} | "
            f"Fair: ${results['expected_price']:.2f} | "
            f"Range: "
            f"${results['lower_bound']:.2f} - "
            f"${results['upper_bound']:.2f} | "
            f"Vol: {volatility:.6f}"
        )


if __name__ == "__main__":
    asyncio.run(main())