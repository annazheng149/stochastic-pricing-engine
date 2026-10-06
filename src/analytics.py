import numpy as np

class MarketAnalytics:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.prices = []

    def add_price(self, price: float):
        self.prices.append(price)
        
        #Only keep the most recent prices
        if len(self.prices) > self.window_size:
            self.prices.pop(0)

    def calculate_returns(self):
        if len(self.prices) < 2:
            return np.array([])

        prices = np.array(self.prices)

        return np.diff(np.log(prices))

    def calculate_volatility(self):
        returns = self.calculate_returns()

        if len(returns) < 2:
            return 0.0

        return np.std(returns, ddof = 1)