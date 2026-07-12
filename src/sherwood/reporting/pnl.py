from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List


@dataclass
class DailySnapshot:
    date: date
    equity: float
    cash: float
    pnl_day: float
    pnl_total: float
    num_positions: int
    gross_exposure: float


class PnLTracker:
    def __init__(self, output_path: str = "logs/pnl.csv") -> None:
        self._path = Path(output_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._snapshots: List[DailySnapshot] = []
        self._initial_equity: float | None = None
        self._prev_equity: float | None = None

    def record(self, snap: DailySnapshot) -> None:
        if self._initial_equity is None:
            self._initial_equity = snap.equity
        self._snapshots.append(snap)
        self._prev_equity = snap.equity
        self._write_row(snap)

    def _write_row(self, snap: DailySnapshot) -> None:
        write_header = not self._path.exists()
        with open(self._path, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow([
                    "date", "equity", "cash", "pnl_day", "pnl_total",
                    "num_positions", "gross_exposure", "return_pct",
                ])
            ret_pct = (
                snap.pnl_day / (snap.equity - snap.pnl_day)
                if snap.equity != snap.pnl_day else 0.0
            )
            writer.writerow([
                snap.date, f"{snap.equity:.2f}", f"{snap.cash:.2f}",
                f"{snap.pnl_day:.2f}", f"{snap.pnl_total:.2f}",
                snap.num_positions, f"{snap.gross_exposure:.2f}",
                f"{ret_pct:.6f}",
            ])

    def summary(self) -> Dict[str, float]:
        if not self._snapshots:
            return {}
        equities = [s.equity for s in self._snapshots]
        returns = [
            (equities[i] - equities[i - 1]) / equities[i - 1]
            for i in range(1, len(equities))
        ]
        total_return = (equities[-1] / equities[0] - 1) if equities[0] else 0
        return {
            "total_return": total_return,
            "peak_equity": max(equities),
            "trough_equity": min(equities),
            "trading_days": len(self._snapshots),
        }
