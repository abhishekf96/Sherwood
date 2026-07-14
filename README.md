# Pickles

Algorithmic trading agent for U.S. equities. S&P 500 universe, paper trading via Alpaca.

Strategies: momentum, mean reversion, statistical pairs, event drift, vol surface.

Signal flow:

```
  Alpaca data → normalizer → signal engine → portfolio builder → risk gate → Alpaca execution
```

## Quickstart

```
pip install -e .
cp .env.example .env
make paper
```

## Strategies

| Strategy | Universe | Frequency |
|---|---|---|
| Cross-sect. momentum | S&P 500 | Monthly |
| Mean reversion | Liquid equities | Intraday |
| Statistical pairs | Correlated pairs | Intraday |
| Event drift | Earnings calendar | Event-driven |
| Volatility surface | Equity options | Tick |

## Config

See `config/default.yaml`. Capital, universe, broker.

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
