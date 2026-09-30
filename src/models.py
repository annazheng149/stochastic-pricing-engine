from datetime import datetime
from pydantic import BaseModel, Field


class MarketTick(BaseModel):
    timestamp: datetime
    symbol: str
    price: float = Field(gt=0)
    volume: int = Field(ge=0)