# Pickles

Algorithmic trading agent. S&P 500 universe, paper trading via Alpaca.

Strategies: momentum, mean reversion, statistical pairs, event drift, vol surface.

## Quickstart

```
pip install -e .
cp .env.example .env
make paper
```

## Config

Edit `config/default.yaml` to set capital, universe, and broker.
