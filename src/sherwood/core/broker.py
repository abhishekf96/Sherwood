from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any

from structlog import get_logger

log = get_logger(__name__)


@dataclass
class Position:
    symbol: str
    qty: int
    avg_cost: float
    market_value: float
    unrealized_pnl: float


@dataclass
class Account:
    cash: float
    equity: float
    buying_power: float
    positions: list[Position]


class BrokerAdapter(abc.ABC):
    @abc.abstractmethod
    async def get_account(self) -> Account: ...

    @abc.abstractmethod
    async def submit_order(
        self,
        symbol: str,
        qty: int,
        side: str,
        order_type: str = "market",
        limit_price: float | None = None,
        time_in_force: str = "day",
    ) -> str: ...

    @abc.abstractmethod
    async def cancel_order(self, order_id: str) -> bool: ...

    @abc.abstractmethod
    async def get_positions(self) -> list[Position]: ...


class AlpacaAdapter(BrokerAdapter):
    def __init__(self, api_key: str, secret_key: str, base_url: str) -> None:
        import alpaca_trade_api as tradeapi
        self._api = tradeapi.REST(api_key, secret_key, base_url)

    async def get_account(self) -> Account:
        acct = self._api.get_account()
        positions = await self.get_positions()
        return Account(
            cash=float(acct.cash),
            equity=float(acct.equity),
            buying_power=float(acct.buying_power),
            positions=positions,
        )

    async def submit_order(self, symbol, qty, side, order_type="market",
                           limit_price=None, time_in_force="day") -> str:
        kwargs: dict[str, Any] = dict(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
        )
        if limit_price is not None:
            kwargs["limit_price"] = str(limit_price)
        order = self._api.submit_order(**kwargs)
        log.info("order_submitted", order_id=order.id, symbol=symbol, qty=qty, side=side)
        return order.id

    async def cancel_order(self, order_id: str) -> bool:
        self._api.cancel_order(order_id)
        return True

    async def get_positions(self) -> list[Position]:
        raw = self._api.list_positions()
        return [
            Position(
                symbol=p.symbol,
                qty=int(p.qty),
                avg_cost=float(p.avg_entry_price),
                market_value=float(p.market_value),
                unrealized_pnl=float(p.unrealized_pl),
            )
            for p in raw
        ]
