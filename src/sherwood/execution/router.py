from __future__ import annotations

from typing import Any

from structlog import get_logger

from sherwood.core.broker import BrokerAdapter
from sherwood.core.engine import OrderEvent, FillEvent
from sherwood.execution.slippage import SlippageModel

log = get_logger(__name__)


class ExecutionRouter:
    def __init__(self, adapters: dict[str, BrokerAdapter],
                 slippage_model: SlippageModel | None = None) -> None:
        self._adapters = adapters
        self._slippage = slippage_model or SlippageModel()
        self._primary = list(adapters.keys())[0]

    def _score_venue(self, venue: str, symbol: str) -> float:
        return 1.0

    async def route(self, order: OrderEvent) -> FillEvent | None:
        best_venue = max(
            self._adapters,
            key=lambda v: self._score_venue(v, order.symbol),
        )
        adapter = self._adapters[best_venue]

        adjusted_price = None
        if order.limit_price is not None:
            adjusted_price = self._slippage.adjust(
                order.limit_price, order.side, order.qty
            )

        try:
            order_id = await adapter.submit_order(
                symbol=order.symbol,
                qty=order.qty,
                side=order.side,
                order_type=order.order_type,
                limit_price=adjusted_price,
            )
            log.info("order_routed", venue=best_venue, order_id=order_id,
                     symbol=order.symbol)
            return None  # fill comes back async via broker callback
        except Exception:
            log.exception("order_failed", symbol=order.symbol, venue=best_venue)
            return None
