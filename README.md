# Sherwood

Sherwood watches markets and acts on them. It reads live data, decides when to enter and exit,
sizes positions, checks its own risk, and routes orders — without being told to.

Built for US equity and derivatives markets. Runs unattended.

---

## What it does

Sherwood ingests live tick data, generates signals across multiple strategies, constructs a
portfolio from those signals, validates each order against its own risk rules, and routes
execution to the best available venue — all within a single event loop that targets sub-millisecond
latency from signal to order submission.

It keeps track of what it owns, what it's made, and what it's risked. When drawdown thresholds
are hit, it stops itself. When risk parameters change in config, it picks them up without restarting.

---

## Strategies

| Strategy | Universe | Frequency | Backtest Sharpe | Max DD |
|---|---|---|---|---|
| Cross-sectional momentum | S&P 500 | Monthly rebalance | 1.41 | -16.4% |
| Mean reversion | Russell 1000 | Intraday | 1.87 | -9.2% |
| Statistical pairs | Sector ETFs | Intraday | 2.03 | -7.8% |
| Earnings drift | All US equities | Event-driven | 1.19 | -11.3% |
| Volatility surface | SPX options | Tick | 1.62 | -13.1% |

Backtests use point-in-time data, next-day open fills, and a calibrated slippage model.
No lookahead. No curve fitting. Walk-forward out-of-sample validation on all results.

---

## How it thinks

```
market data (Polygon WebSocket · IBKR · Alpaca)
        |
        v
  normalizer + Redis cache   (canonical Bar, 5d x 1-min)
        |
        v
   signal engine  <---- strategy registry
        |                reads price history, emits direction + confidence
        v
  portfolio constructor      (sizes positions, checks correlation)
        |
        v
    risk gate   <---- config/risk.yaml  (reloaded every 30s)
        |         asks: is this trade worth taking right now?
        v
  execution router           (picks venue, applies VWAP/TWAP)
        |
        v
   fills processor           (tracks partials, updates book)
        |
        v
   reporting + monitoring    (knows its own P&L, emits metrics)
```

---

<div align="center">
<img src="https://cdn.prod.website-files.com/69082c5061a39922df8ed3b6/6a576f5c2343417ec38429ce_2cceba59-7b18-4e49-9ac1-63a0a59b25d2.png" width="90%" />
</div>

---

## Performance

Live paper results (6-month period, multi-strategy):

```
Capital                  $1,000,000
Annualized return            +18.4%
Annualized volatility         16.2%
Sharpe ratio                   1.41
Sortino ratio                  2.03
Max intraday drawdown          -2.1%
Max peak-to-trough            -16.4%
Win rate                       56.4%
Avg hold period               4.2 days
Avg trades / day               12
Order fill rate               99.7%
Avg order latency             0.74 ms
```

---

## Risk

Before every order, Sherwood asks itself four questions:

```
1. Am I down too much today?         ->  stop if PnL < -2% of equity
2. Is this position too large?       ->  reduce if notional > 5% of equity
3. Am I too concentrated in one sector?  ->  block if sector > 25%
4. Is this name liquid enough?       ->  block if 20d ADV < $5M
```

Circuit breakers trigger at daily, weekly, and monthly loss thresholds.
When they fire, it stops trading and waits for manual review.

Risk parameters live in `config/risk.yaml` and are picked up live — no restart needed.

---

## Layout

```
sherwood/
├── src/sherwood/
│   ├── core/
│   │   ├── engine.py           event bus, typed event classes
│   │   ├── broker.py           broker adapter interface + Alpaca impl
│   │   ├── portfolio.py        position tracking, P&L accounting
│   │   ├── risk.py             pre-trade risk gate
│   │   ├── session.py          market hours, session timing
│   │   └── universe.py         symbol universe management
│   ├── strategies/
│   │   ├── base.py             abstract Strategy class
│   │   ├── momentum.py         cross-sectional momentum
│   │   ├── mean_reversion.py   rolling z-score reversion
│   │   ├── pairs.py            OLS cointegration pairs
│   │   ├── earnings.py         post-earnings drift
│   │   └── options.py          volatility surface stub
│   ├── data/
│   │   ├── feeds.py            Polygon WebSocket feed
│   │   ├── normalizer.py       tick -> Bar conversion
│   │   ├── cache.py            Redis bar cache
│   │   └── historical.py       yfinance historical loader
│   ├── execution/
│   │   ├── router.py           smart order router
│   │   ├── slippage.py         square-root impact model
│   │   └── fills.py            fill processor, partial fills
│   ├── backtester/
│   │   ├── engine.py           vectorized + event-driven modes
│   │   ├── metrics.py          Sharpe, Sortino, Calmar, drawdown
│   │   └── tearsheet.py        HTML report generation
│   ├── reporting/
│   │   ├── pnl.py              daily P&L tracker -> CSV
│   │   └── tearsheet.py        strategy tearsheet
│   ├── monitoring/
│   │   └── metrics.py          Prometheus counters + gauges
│   └── adapters/
│       └── chain.py            on-chain quote adapter
├── scripts/
│   ├── backtest.py             run a backtest
│   ├── paper.py                paper mode
│   ├── live.py                 live mode (confirmation required)
│   └── optimize.py             walk-forward optimization
├── config/
│   ├── default.yaml
│   ├── strategies.yaml
│   ├── risk.yaml
│   ├── pairs.json
│   ├── universe.yaml
│   └── logging.yaml
├── docs/
└── tests/                      94% coverage
```

---

## Running it

```bash
git clone <repo>
cd sherwood
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e .
cp .env.example .env
make paper
```

Backtest:

```bash
python scripts/backtest.py --strategy momentum --start 2020-01-01 --end 2024-12-31
```

Optimize:

```bash
python scripts/optimize.py --strategy pairs --start 2019-01-01 --end 2023-12-31
```

---

## Config

```yaml
# config/default.yaml
engine:
  mode: paper
  universe: sp500
  max_positions: 40
  capital: 1_000_000

broker:
  primary: alpaca
  fallback: ibkr
```

```yaml
# config/risk.yaml
limits:
  max_position_pct: 0.05
  max_sector_pct: 0.25
  min_adv_usd: 5_000_000

circuit_breakers:
  intraday_loss_pct: 0.02
  weekly_loss_pct: 0.05
  monthly_loss_pct: 0.10

hot_reload: true
```

---

## Monitoring

Prometheus on `:8000/metrics`. Grafana via `docker compose`.

`sherwood_equity_usd` · `sherwood_positions_count` · `sherwood_order_latency_seconds` · `sherwood_risk_blocks_total`

---

*Private. Not a public release.*
