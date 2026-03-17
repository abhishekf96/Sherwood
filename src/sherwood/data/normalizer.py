from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class Bar:
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    timestamp: float
    vwap: float | None = None


def normalize_polygon_bar(raw: dict) -> Bar:
    return Bar(
        symbol=raw["T"],
        open=raw["o"],
        high=raw["h"],
        low=raw["l"],
        close=raw["c"],
        volume=raw["v"],
        timestamp=raw["t"] / 1000,
        vwap=raw.get("vw"),
    )


def bars_to_ohlcv(bars: list[Bar]) -> pd.DataFrame:
    records = [
        {"timestamp": b.timestamp, "symbol": b.symbol,
         "open": b.open, "high": b.high, "low": b.low,
         "close": b.close, "volume": b.volume}
        for b in bars
    ]
    df = pd.DataFrame(records)
    if df.empty:
        return df
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
    return df.set_index("timestamp").pivot(columns="symbol", values="close")
