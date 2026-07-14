# Pickles

Algorithmic trading agent. S&P 500 universe, paper trading via Alpaca.

Strategies: momentum, mean reversion, statistical pairs, event drift, vol surface.

## Quickstart

```
pip install -e .
cp .env.example .env
make paper      # paper trading
make backtest   # run backtest suite
make test       # unit tests
```

## Config

```yaml
engine:
  mode: paper
  capital: 1_000_000
  universe: sp500

broker:
  primary: alpaca
  fallback: ibkr
```

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
