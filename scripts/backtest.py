"""Run a single strategy backtest and print the tearsheet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sherwood.backtester.engine import Backtester
from sherwood.backtester.metrics import compute_metrics
from sherwood.backtester.report import generate_tearsheet
from sherwood.data.historical import load_universe
from sherwood.strategies import MomentumStrategy, MeanReversionStrategy
from sherwood.strategies.pairs import PairsStrategy
from sherwood.utils.logger import setup_logging


STRATEGY_MAP = {
    "momentum": MomentumStrategy,
    "mean_reversion": MeanReversionStrategy,
    "pairs": PairsStrategy,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Sherwood backtester")
    parser.add_argument("--strategy", required=True, choices=STRATEGY_MAP)
    parser.add_argument("--start", default="2020-01-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument("--capital", type=float, default=1_000_000)
    parser.add_argument("--config", default="config/strategies.yaml")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    setup_logging()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    strategy_cfg = cfg.get("strategies", {}).get(args.strategy, {})
    strategy = STRATEGY_MAP[args.strategy](strategy_cfg)

    print(f"Loading universe {args.start} → {args.end}...")
    data = load_universe(start=args.start, end=args.end)

    print(f"Running {args.strategy} backtest on {len(data.columns)} symbols...")
    bt = Backtester(strategy, capital=args.capital)
    result = bt.run(data)

    metrics = compute_metrics(result.returns)
    print("\n── Results ───────────────────────────────────")
    for k, v in metrics.items():
        print(f"  {k:<28} {v:>10.4f}")

    generate_tearsheet(result)
    print("\nTearsheet written to reports/tearsheet.html")

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)


if __name__ == "__main__":
    main()
