import asyncio

from src.stream import load_market_data, stream_market_data
from src.analytics import MarketAnalytics
from src.simulation import MonteCarloSimulator
from src.pricing import PricingEngine
from src.risk import RiskEngine, RiskStatus
from src.forecast_manager import ForecastManager


async def main():
    ticks = load_market_data("data/market_ticks.csv")

    analytics = MarketAnalytics(window_size=100)

    simulator = MonteCarloSimulator(num_simulations=10_000, num_steps=60)

    pricing_engine = PricingEngine( 
        base_spread=0.0005,
        volatility_multiplier=2.0
    )

    risk_engine = RiskEngine(
        volatility_warning=0.001,
        volatility_halt=0.002,
        mad_warning=0.50,
        mad_halt=1.00
    )
    
    forecast_manager = ForecastManager(horizon_minutes=60)


    print("Starting market data stream...\n")

    async for tick in stream_market_data(ticks, delay=0.5):
        
        analytics.add_price(tick.price)

        due_forecasts = forecast_manager.get_due_forecasts(
        tick.timestamp
    )

        for forecast in due_forecasts:

            risk_engine.add_prediction_error(
                predicted_price=forecast.predicted_price,
                actual_price=tick.price
            )

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

        risk_status = risk_engine.check_risk(
            volatility=volatility
        )

        if risk_status == RiskStatus.HALTED:

            print(
                f"{tick.symbol} | "
                f"${tick.price:.2f} | "
                f"RISK: HALTED | "
                f"Circuit breaker triggered"
            )

            continue

        path = simulator.simulate(
            current_price=tick.price,
            drift=drift,
            volatility=volatility
        )

        pricing = pricing_engine.calculate_prices(
            current_price=tick.price,
            price_paths=path,
            volatility=volatility
        )

        forecast_manager.add_forecast(
            timestamp=tick.timestamp,
            predicted_price=pricing["fair_price"]
        )

        results = simulator.summarize(path)
        
        print(
            f"{tick.symbol} | "
            f"Current: ${tick.price:.2f} | "
            f"Fair: ${pricing['fair_price']:.2f} | "
            f"Bid: ${pricing['bid_price']:.2f} | "
            f"Ask: ${pricing['ask_price']:.2f} | "
            f"P(Up): {pricing['probability_up']:.1%}"
        )


if __name__ == "__main__":
    asyncio.run(main())