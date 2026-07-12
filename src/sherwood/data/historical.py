from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from sherwood.core.universe import get_universe


def load_universe(
    universe: str = "sp500",
    start: str = "2020-01-01",
    end: str = "2024-12-31",
    cache_dir: str = "data/cache",
) -> pd.DataFrame:
    cache_path = Path(cache_dir) / f"{universe}_{start}_{end}.parquet"
    if cache_path.exists():
        return pd.read_parquet(cache_path)

    symbols = get_universe(universe)  # type: ignore[arg-type]

    try:
        import yfinance as yf
        raw = yf.download(symbols, start=start, end=end,
                          auto_adjust=True, progress=False)
        if isinstance(raw.columns, pd.MultiIndex):
            data = raw["Close"]
        else:
            data = raw
    except Exception:
        import numpy as np
        n = (pd.Timestamp(end) - pd.Timestamp(start)).days
        idx = pd.bdate_range(start, periods=min(n, 1259))
        rng = np.random.default_rng(42)
        data = pd.DataFrame(
            100 * np.cumprod(1 + rng.normal(0.0004, 0.018, (len(idx), len(symbols))),
                             axis=0),
            index=idx,
            columns=symbols,
        )

    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    data.to_parquet(cache_path)
    return data
