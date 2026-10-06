from datetime import timedelta

from src.forecast import Forecast


class ForecastManager:

    def __init__(self, horizon_minutes: int = 60):
        self.horizon = timedelta(
            minutes=horizon_minutes
        )

        self.forecasts = []

    def add_forecast(
        self,
        timestamp,
        predicted_price
    ):

        forecast = Forecast(
            created_at=timestamp,
            target_time=timestamp + self.horizon,
            predicted_price=predicted_price
        )

        self.forecasts.append(forecast)

    def get_due_forecasts(self, current_time):

        due = []

        remaining = []

        for forecast in self.forecasts:

            if current_time >= forecast.target_time:
                due.append(forecast)
            else:
                remaining.append(forecast)

        self.forecasts = remaining

        return due