import pytest
from unittest.mock import AsyncMock, MagicMock

from sherwood.core.engine import OrderEvent
from sherwood.execution.fills import FillProcessor
from sherwood.execution.slippage import SlippageModel


def test_fill_processor_tracks_fills():
    received = []
    fp = FillProcessor(on_fill=received.append)
    fp.register_order("ord1", "AAPL", 100, "buy")
    event = fp.process_fill("ord1", 100, 150.25, 1700000000.0, commission=1.5)
    assert event is not None
    assert event.symbol == "AAPL"
    assert event.avg_price == 150.25
    assert len(received) == 1


def test_fill_processor_ignores_unknown_orders():
    fp = FillProcessor(on_fill=lambda e: None)
    result = fp.process_fill("unknown", 10, 100.0, 0.0)
    assert result is None


def test_slippage_buy_increases_price():
    m = SlippageModel(bps=5.0)
    assert m.adjust(100.0, "buy", 10) > 100.0


def test_slippage_sell_decreases_price():
    m = SlippageModel(bps=5.0)
    assert m.adjust(100.0, "sell", 10) < 100.0


def test_slippage_market_impact_scales_with_participation():
    m = SlippageModel(bps=1.0, market_impact_coeff=0.1)
    small = m.adjust(100.0, "buy", 100, adv=10_000_000)
    large = m.adjust(100.0, "buy", 500_000, adv=10_000_000)
    assert large > small
