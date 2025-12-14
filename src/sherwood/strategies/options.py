from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import norm

from sherwood.strategies.base import Strategy
from sherwood.core.engine import SignalEvent


@dataclass
class OptionContract:
    symbol: str
    expiry: str
    strike: float
    option_type: str  # call | put
    bid: float
    ask: float
    iv: float
    delta: float
    theta: float
    vega: float


def black_scholes_delta(S: float, K: float, T: float, r: float,
                        sigma: float, option_type: str = "call") -> float:
    if T <= 0 or sigma <= 0:
        return 0.0
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return float(norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1)


class VolatilitySurfaceStrategy(Strategy):
    name = "options_vol"

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.underlying: str = config.get("underlying", "SPX")
        self.target_delta: float = config.get("target_delta", 0.15)
        self.target_dte: int = config.get("target_dte", 30)
        self.max_vega: float = config.get("max_vega", 50_000)

    def generate_signals(self, data: pd.DataFrame) -> list[SignalEvent]:
        return []
