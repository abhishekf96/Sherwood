from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Core equity metrics
# meow
equity_usd        = Gauge("pickles_equity_usd", "Total portfolio equity in USD")
pnl_today_usd     = Gauge("pickles_pnl_today_usd", "Intraday P&L in USD")
drawdown_pct      = Gauge("pickles_drawdown_pct", "Current drawdown from peak equity")
open_positions    = Gauge("pickles_open_positions", "Number of open positions")

# On-chain metrics
chain_wallet_bal  = Gauge("pickles_chain_wallet_balance_usd", "Agent wallet balance USD equivalent")
chain_positions   = Gauge("pickles_chain_positions_count", "Number of on-chain token positions")
chain_fills       = Counter("pickles_chain_fills_total", "Total on-chain order fills")
chain_errors      = Counter("pickles_chain_errors_total", "On-chain submission errors", ["reason"])

# Execution metrics
orders_total      = Counter("pickles_orders_total", "Orders submitted", ["side", "venue"])
order_latency     = Histogram("pickles_order_latency_seconds", "Order submission latency",
                               buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0])

# Risk metrics
risk_blocks       = Counter("pickles_risk_blocks_total", "Orders blocked by risk gate", ["reason"])
risk_reduces      = Counter("pickles_risk_reduces_total", "Orders reduced by risk gate")

# Sentiment metrics
sentiment_fetches = Counter("pickles_sentiment_fetches_total", "Sentiment fetch calls", ["source"])
sentiment_score   = Gauge("pickles_sentiment_score", "Latest blended sentiment score", ["symbol"])


def start(port: int = 8000) -> None:
    start_http_server(port)
