import numpy as np
import pandas as pd
import pytest

from sherwood.strategies.momentum import MomentumStrategy
from sherwood.strategies.mean_reversion import MeanReversionStrategy


def make_price_data(symbols: list[str], n: int = 300) -> pd.DataFrame:
    np.random.seed(42)
    data = {}
    for sym in symbols:
        returns = np.random.normal(0.0005, 0.015, n)
        prices = 100 * np.cumprod(1 + returns)
        data[sym] = prices
    idx = pd.date_range("2023-01-01", periods=n, freq="B")
    return pd.DataFrame(data, index=idx)


def test_momentum_generates_signals():
    symbols = [f"SYM{i}" for i in range(30)]
    data = make_price_data(symbols)
    strategy = MomentumStrategy({"lookback": 252, "top_n": 5, "enabled": True})
    signals = strategy.generate_signals(data)
    assert len(signals) > 0
    for sig in signals:
        assert sig.strategy == "momentum"
        assert sig.direction in (1, -1)
        assert 0.0 <= sig.confidence <= 1.0


def test_momentum_requires_enough_history():
    symbols = ["AAPL", "MSFT"]
    data = make_price_data(symbols, n=100)
    strategy = MomentumStrategy({"lookback": 252, "top_n": 2, "enabled": True})
    signals = strategy.generate_signals(data)
    assert signals == []


def test_mean_reversion_detects_extremes():
    np.random.seed(0)
    idx = pd.date_range("2024-01-01", periods=100, freq="B")
    prices = np.concatenate([
        np.linspace(100, 110, 80),
        np.linspace(110, 130, 20),
    ])
    data = pd.DataFrame({"AAPL": prices}, index=idx)
    strategy = MeanReversionStrategy({"lookback": 20, "zscore_entry": 1.5})
    signals = strategy.generate_signals(data)
    short_signals = [s for s in signals if s.direction == -1]
    assert len(short_signals) > 0


def test_mean_reversion_confidence_bounded():
    data = make_price_data(["X", "Y"], n=100)
    strategy = MeanReversionStrategy({"lookback": 20, "zscore_entry": 1.0})
    for sig in strategy.generate_signals(data):
        assert 0.0 <= sig.confidence <= 1.0

