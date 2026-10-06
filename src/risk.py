import numpy as np
from enum import Enum

class RiskStatus(Enum):
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    HALTED = "HALTED"

class RiskEngine:

    def __init__(
            self,
            volatility_warning:float = 0.001,
            volatility_halt: float = 0.002,
            mad_warning: float = 0.50,
            mad_halt: float = 1.00
    ):

        self.volatility_warning = volatility_warning
        self.volatility_halt = volatility_halt

        self.mad_warning = mad_warning
        self.mad_halt = mad_halt

        self.prediction_errors = []

    def add_prediction_error(
            self,
            predicted_price: float,
            actual_price: float
    ):
        error = abs(actual_price - predicted_price)

        self.prediction_errors.append(error)

        #Only keep recent errors
        if len(self.prediction_errors) > 100:
            self.prediction_errors.pop(0)

    def calculate_mad(self) -> float:

        if len(self.prediction_errors) == 0:
            return 0.0

        return float(
            np.mean(self.prediction_errors)
        )

    def check_risk(
            self,
            volatility: float
    ) -> RiskStatus:

        mad = self.calculate_mad()

        #Most severe conditions first
        if (
            volatility >= self.volatility_halt
            or mad >= self.mad_halt
        ):
            return RiskStatus.HALTED

        if (
            volatility >= self.volatility_warning
            or mad >= self.mad_warning
        ):
            return RiskStatus.WARNING

        return RiskStatus.NORMAL