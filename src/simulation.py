import numpy as np

class MonteCarloSimulator:

    def __init__(
            self,
            num_simulations: int = 10_000,
            num_steps: int = 60
    ):
        self.num_simulations = num_simulations
        self.num_steps = num_steps

    def simulate(
            self, 
            current_price: float,
            drift: float,
            volatility: float
    ) -> np.ndarray:

        #Generate all random shocks at once
        random_shocks = np.random.normal(
            loc = 0.0,
            scale = 1.0,
            size = (self.num_simulations, self.num_steps)
        )

        #GBM log-return for every simulation and time step
        simulated_returns = (
            drift - 0.5 * volatility ** 2
        ) + volatility * random_shocks

        #Convert resturns into price paths
        cumulative_returns = np.cumsum(
            simulated_returns,
            axis = 1
        )

        price_paths = current_price * np.exp(
            cumulative_returns
        )

        return price_paths

    def summarize(self, price_paths: np.ndarray) -> dict:

        final_prices = price_paths[:, 1]

        return {
            "expected_price": np.mean(final_prices),
            "median_price": np.median(final_prices),
            "lower_bound": np.percentile(final_prices, 5),
            "upper_bound": np.percentile(final_prices, 95),
            "min_price": np.min(final_prices),
            "max_price": np.max(final_prices)
        }