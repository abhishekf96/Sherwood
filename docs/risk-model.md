# Risk Model

## Pre-trade Checks

Every `OrderEvent` passes through the risk gate before reaching the execution router.
Checks run in priority order; the first failure short-circuits the rest.

1. **Intraday drawdown** — if unrealized + realized P&L for the session drops below
   `intraday_loss_pct * equity`, all new orders are blocked until the next session open.

2. **Position size** — if the order notional would exceed `max_position_pct * equity`,
   the quantity is reduced to fit within the limit (REDUCE decision).

3. **Correlation gate** (optional) — computes the marginal beta contribution of the
   proposed position. Blocks if portfolio beta would exceed `max_net_leverage`.

4. **Liquidity filter** — blocks symbols with 20-day ADV below `min_adv_usd`.

## Circuit Breakers

| Trigger | Action |
|---|---|
| Intraday loss > 2% | Block all new orders for session |
| Weekly loss > 5% | Reduce position limits by 50% |
| Monthly loss > 10% | Full stop, alert, await manual review |

## Hot Reload

The risk gate watches `config/risk.yaml` for changes and applies new parameters
within `reload_interval_seconds` (default 30s) without restarting the engine.
This allows real-time parameter adjustment during live trading.
