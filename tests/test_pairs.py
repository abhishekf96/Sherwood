import numpy as np
import pandas as pd
import pytest

from sherwood.strategies.pairs import PairsStrategy


def make_cointegrated_pair(n: int = 200) -> pd.DataFrame:
    np.random.seed(5)
    x = np.cumsum(np.random.normal(0, 1, n))
    y = 2.5 * x + np.random.normal(0, 0.5, n)
    idx = pd.bdate_range("2023-01-01", periods=n)
    return pd.DataFrame({"LEG1": 100 + y, "LEG2": 100 + x}, index=idx)


def test_pairs_no_pairs_file_returns_empty():
    strategy = PairsStrategy({"pairs_file": "nonexistent.json", "enabled": True})
    data = make_cointegrated_pair()
    signals = strategy.generate_signals(data)
    assert signals == []


def test_pairs_hedge_ratio_positive():
    from sherwood.strategies.pairs import PairsStrategy
    s = PairsStrategy({"pairs_file": "nonexistent.json"})
    data = make_cointegrated_pair()
    hr = s._compute_hedge_ratio(data["LEG1"], data["LEG2"])
    assert hr > 0


def test_zscore_stationary():
    from sherwood.strategies.pairs import PairsStrategy
    s = PairsStrategy({"pairs_file": "nonexistent.json"})
    data = make_cointegrated_pair(300)
    hr = s._compute_hedge_ratio(data["LEG1"], data["LEG2"])
    z = s._spread_zscore(data["LEG1"], data["LEG2"], hr)
    assert isinstance(z, float)
    assert abs(z) < 10
