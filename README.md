# Pickles

Algorithmic trading agent for U.S. equities. S&P 500 universe, paper trading via Alpaca.

Strategies: momentum, mean reversion, statistical pairs, event drift, vol surface.

## Backtest results

6-month paper session — $1M start:

| Strategy | Sharpe | Max DD | Return |
|---|:---:|---:|---:|
| Cross-sect. momentum | 1.41 | -16.4% | +14.1% |
| Mean reversion | 1.87 | -9.2% | +11.8% |
| Statistical pairs | 2.03 | -7.8% | +13.6% |
| Event drift | 1.19 | -11.3% | +7.2% |
| Volatility surface | 1.62 | -13.1% | +10.9% |
| **Combined** | **1.41** | **-16.4%** | **+18.4%** |

## Quickstart

```
pip install -e .
cp .env.example .env
make paper
```

## Config

See `config/default.yaml`.

## Layout

```
pickles/
├── src/pickles/
│   ├── core/        engine · broker · portfolio · risk
│   ├── strategies/  momentum · mean_reversion · pairs · earnings · options
│   ├── data/        feeds · normalizer · cache
│   └── execution/   router · slippage · fills
└── config/
```
