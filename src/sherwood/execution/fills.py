from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from structlog import get_logger

from sherwood.core.engine import FillEvent

log = get_logger(__name__)


class FillProcessor:
    def __init__(self, on_fill: Callable[[FillEvent], None]) -> None:
        self._on_fill = on_fill
        self._pending: dict[str, dict] = {}

    def register_order(self, order_id: str, symbol: str,
                       expected_qty: int, side: str) -> None:
        self._pending[order_id] = {
            "symbol": symbol,
            "expected_qty": expected_qty,
            "filled_qty": 0,
            "side": side,
        }

    def process_fill(self, order_id: str, fill_qty: int,
                     fill_price: float, timestamp: float,
                     commission: float = 0.0) -> FillEvent | None:
        if order_id not in self._pending:
            log.warning("unknown_order", order_id=order_id)
            return None

        order = self._pending[order_id]
        order["filled_qty"] += fill_qty

        event = FillEvent(
            order_id=order_id,
            symbol=order["symbol"],
            qty=fill_qty,
            avg_price=fill_price,
            side=order["side"],
            timestamp=timestamp,
            commission=commission,
        )
        self._on_fill(event)

        if order["filled_qty"] >= order["expected_qty"]:
            del self._pending[order_id]

        return event
