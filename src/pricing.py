import numpy as np

class PricingEngine:

    def __init__ (
            self,
            base_spread: float = 0.0005,
            volatility_multiplier: float = 0.2
    ):
        self.base_spread = base_spread
        self.volatility_multiplier = volatility_multiplier

    def calculate_prices(
            self,
            current_price: float,
            price_paths: np.ndarray,
            volatility: float
    )-> dict:

        final_prices = price_paths[:, -1]

        #Estimated fair value
        fair_price = np.mean(final_prices)

        #Prbability the future price finishes above current price
        probability_up = np.mean (
            final_prices > current_price
        )

        # Increase spread when volatility increases
        spread_percentage = (
            self.base_spread
            + self.volatility_multiplier * volatility
        )

        half_spread = (
            fair_price * spread_percentage / 2
        )

        bid_price = fair_price - half_spread
        ask_price = fair_price + half_spread

        return {
            "fair_price": fair_price,
            "bid_price": bid_price,
            "ask_price": ask_price,
            "spread": ask_price - bid_price,
            "probability_up": probability_up
        }