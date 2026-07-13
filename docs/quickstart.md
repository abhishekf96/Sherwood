# Quickstart

## Prerequisites

- Python 3.11+
- Redis (for bar cache)
- Alpaca paper trading account or Interactive Brokers paper account

## Install

```bash
git clone <repo>
cd sherwood
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env
```

Fill in `.env` with your broker credentials.

## Paper trading

```bash
make paper
# or
python scripts/paper.py --config config/default.yaml
```

The engine will connect to your broker's paper API, subscribe to the configured
universe, and begin generating and executing signals in real time.

## Run a backtest

```bash
python scripts/backtest.py --strategy momentum --start 2020-01-01 --end 2024-12-31
```

Output:

```
── Results ────────────────────────────────────
  Annualized Return            +0.1841
  Annualized Volatility         0.1623
  Sharpe Ratio                  1.4100
  Sortino Ratio                 2.0317
  Calmar Ratio                  1.1230
  Max Drawdown                 -0.1640
  Win Rate                      0.5640
  Profit Factor                 1.4420
```

Tearsheet saved to `reports/tearsheet.html`.

## Run optimization

```bash
python scripts/optimize.py --strategy momentum --start 2019-01-01 --end 2023-12-31
```

Uses walk-forward validation with 1-year training windows and 63-day test windows.
