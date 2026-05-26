# Contributing

## Strategy Contributions

New strategies must:
1. Extend `Strategy` base class
2. Implement `generate_signals(data: pd.DataFrame) -> list[SignalEvent]`
3. Pass backtester smoke tests (minimum 2 years of data, Sharpe > 0.5)
4. Include at least 5 unit tests in `tests/test_strategies.py`
5. Document parameters in `docs/signals.md`

## Code Standards

- Python 3.11+, typed throughout (`mypy --strict`)
- `ruff` for linting (config in `pyproject.toml`)
- All public functions require docstrings
- No third-party dependencies without prior discussion

## Pull Requests

Open against `main`. Include backtest results (Sharpe, max drawdown, win rate)
in the PR description for any strategy changes.
