import pytest
from sherwood.core.portfolio import Portfolio


def test_initial_portfolio_state():
    p = Portfolio(initial_capital=100_000)
    assert p.equity == 100_000
    assert p._cash == 100_000
    assert len(p._positions) == 0


def test_buy_increases_position():
    p = Portfolio(100_000)
    p.apply_fill("AAPL", 10, 150.0, "buy")
    assert "AAPL" in p._positions
    assert p._positions["AAPL"]["qty"] == 10


def test_sell_removes_position():
    p = Portfolio(100_000)
    p.apply_fill("AAPL", 10, 150.0, "buy")
    p.apply_fill("AAPL", 10, 160.0, "sell")
    assert "AAPL" not in p._positions
    assert p._realized_pnl == pytest.approx(100.0)


def test_price_update_affects_equity():
    p = Portfolio(100_000)
    p.apply_fill("MSFT", 100, 300.0, "buy")
    p.update_price("MSFT", 310.0)
    assert p.equity > 100_000


def test_snapshot_contains_positions():
    p = Portfolio(50_000)
    p.apply_fill("NVDA", 5, 800.0, "buy")
    snap = p.snapshot()
    assert "NVDA" in snap.positions
    assert snap.equity > 0


def test_commission_reduces_cash():
    p = Portfolio(100_000)
    p.apply_fill("AAPL", 100, 150.0, "buy", commission=2.50)
    assert p._cash == pytest.approx(100_000 - 100 * 150.0 - 2.50)
