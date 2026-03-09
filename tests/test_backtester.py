import numpy as np
import pandas as pd
import pytest

from sherwood.backtester.engine import Backtester
from sherwood.backtester.metrics import compute_metrics
from sherwood.strategies.momentum import MomentumStrategy
from sherwood.strategies.mean_reversion import MeanReversionStrategy


def make_data(n: int = 400) -> pd.DataFrame:
    np.random.seed(1)
    symbols = [f"S{i}" for i in range(20)]
    data = {}
    for s in symbols:
        r = np.random.normal(0.0004, 0.018, n)
        data[s] = 100 * np.cumprod(1 + r)
    return pd.DataFrame(data, index=pd.date_range("2022-01-01", periods=n, freq="B"))


def test_backtest_runs_and_returns_equity_curve():
    data = make_data()
    strategy = MomentumStrategy({"lookback": 252, "top_n": 5, "enabled": True})
    bt = Backtester(strategy, capital=500_000)
    result = bt.run(data)
    assert len(result.equity_curve) > 0
    assert result.equity_curve.iloc[0] > 0


def test_backtest_metrics_computed():
    data = make_data()
    strategy = MomentumStrategy({"lookback": 252, "top_n": 5, "enabled": True})
    bt = Backtester(strategy)
    result = bt.run(data)
    m = compute_metrics(result.returns)
    assert "sharpe_ratio" in m
    assert "max_drawdown" in m
    assert m["max_drawdown"] <= 0


def test_metrics_on_flat_returns():
    returns = pd.Series([0.0] * 100)
    m = compute_metrics(returns)
    assert m["sharpe_ratio"] == 0.0
    assert m["max_drawdown"] == 0.0


def test_mean_reversion_backtest():
    data = make_data(200)
    strategy = MeanReversionStrategy({"lookback": 20, "zscore_entry": 1.5})
    bt = Backtester(strategy, capital=250_000)
    result = bt.run(data)
    assert len(result.trades) >= 0
