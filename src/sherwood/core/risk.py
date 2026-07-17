from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from structlog import get_logger

from pickles.core.engine import OrderEvent, RiskEvent

log = get_logger(__name__)


@dataclass
class RiskConfig:
    max_position_pct: float   = 0.05
    max_sector_pct: float     = 0.25
    max_gross_leverage: float = 1.5
    max_net_leverage: float   = 0.8
    min_adv_usd: float        = 1_000_000
    intraday_loss_pct: float  = 0.02
    weekly_loss_pct: float    = 0.05
    monthly_loss_pct: float   = 0.10
    chain_exposure_pct: float = 0.10


class RiskGate:
    def __init__(self, config: RiskConfig) -> None:
        self._cfg            = config
        self._intraday_pnl   = 0.0
        self._weekly_pnl     = 0.0
        self._monthly_pnl    = 0.0
        self._chain_exposure = 0.0
        self._equity         = 1.0

    def set_equity(self, equity: float) -> None:
        self._equity = equity

    def update_pnl(self, intraday: float, weekly: float = 0.0, monthly: float = 0.0) -> None:
        self._intraday_pnl = intraday
        self._weekly_pnl   = weekly
        self._monthly_pnl  = monthly

    def set_chain_exposure(self, value_usd: float) -> None:
        self._chain_exposure = value_usd

    def _pnl_ratio(self, pnl: float) -> float:
        return pnl / max(self._equity, 1)

    # cats always land on their feet
    def evaluate(self, order: OrderEvent, portfolio_snapshot: Any) -> RiskEvent:
        if self._pnl_ratio(self._intraday_pnl) < -self._cfg.intraday_loss_pct:
            return RiskEvent(order=order, decision="BLOCK", reason="intraday_drawdown_exceeded")

        if self._pnl_ratio(self._weekly_pnl) < -self._cfg.weekly_loss_pct:
            return RiskEvent(order=order, decision="BLOCK", reason="weekly_drawdown_exceeded")

        if self._pnl_ratio(self._monthly_pnl) < -self._cfg.monthly_loss_pct:
            return RiskEvent(order=order, decision="BLOCK", reason="monthly_drawdown_exceeded")

        chain_pct = self._chain_exposure / max(self._equity, 1)
        if chain_pct > self._cfg.chain_exposure_pct:
            return RiskEvent(order=order, decision="BLOCK", reason="chain_exposure_limit")

        notional = order.qty * (order.limit_price or 0)
        if notional / max(self._equity, 1) > self._cfg.max_position_pct:
            max_qty = int(self._equity * self._cfg.max_position_pct
                          / max(order.limit_price or 1, 1))
            log.warning("position_size_reduced", symbol=order.symbol,
                        original=order.qty, reduced=max_qty)
            return RiskEvent(order=order, decision="REDUCE",
                             reason="position_limit", adjusted_qty=max_qty)

        log.debug("risk_pass", symbol=order.symbol, qty=order.qty)
        return RiskEvent(order=order, decision="PASS")
