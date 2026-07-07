# Changelog

## v0.4.0
- Pairs strategy with OLS hedge ratio estimation
- Walk-forward backtester with out-of-sample holdout
- Redis-backed bar cache with configurable TTL
- Prometheus metrics endpoint

## v0.3.0
- Mean reversion strategy with rolling z-score signals
- Slippage model with square-root market impact
- Fill processor with partial fill tracking
- Risk gate hot-reload from config/risk.yaml

## v0.2.0
- Momentum strategy (12-month lookback, long/short)
- Portfolio constructor with position sizing
- Alpaca adapter (paper + live)
- Event bus with typed handlers

## v0.1.0
- Core engine scaffold
- Event types: Tick, Signal, Order, Fill, Risk
- IBKR adapter stub
- Backtester with Monte Carlo drawdown analysis

