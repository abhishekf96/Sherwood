"""Launch Sherwood in live trading mode. Requires confirmed configuration."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def confirm_live() -> bool:
    print("=" * 60)
    print("  WARNING: LIVE TRADING MODE")
    print("  Real orders will be submitted to your broker.")
    print("  Ensure risk parameters are correct before proceeding.")
    print("=" * 60)
    resp = input("\nType 'CONFIRM' to proceed: ").strip()
    return resp == "CONFIRM"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/default.yaml")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()

    if not args.yes and not confirm_live():
        print("Aborted.")
        sys.exit(0)

    from sherwood.core.engine import Engine
    from sherwood.utils.logger import setup_logging

    with open(args.config) as f:
        config = yaml.safe_load(f)

    config.setdefault("engine", {})["mode"] = "live"
    setup_logging()

    engine = Engine(config)
    engine.start()

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        engine.stop()


if __name__ == "__main__":
    main()
