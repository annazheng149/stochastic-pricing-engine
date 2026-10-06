from dataclasses import dataclass
from datetime import datetime


@dataclass
class Forecast:
    created_at: datetime
    target_time: datetime
    predicted_price: float