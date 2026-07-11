from __future__ import annotations

import zoneinfo
from datetime import datetime, time


NY = zoneinfo.ZoneInfo("America/New_York")

SESSION_OPEN = time(9, 30)
SESSION_CLOSE = time(16, 0)
PRE_MARKET_OPEN = time(4, 0)
AFTER_HOURS_CLOSE = time(20, 0)


def is_market_open(dt: datetime | None = None) -> bool:
    now = (dt or datetime.now(NY)).astimezone(NY)
    if now.weekday() >= 5:
        return False
    return SESSION_OPEN <= now.time() <= SESSION_CLOSE


def is_pre_market(dt: datetime | None = None) -> bool:
    now = (dt or datetime.now(NY)).astimezone(NY)
    if now.weekday() >= 5:
        return False
    return PRE_MARKET_OPEN <= now.time() < SESSION_OPEN


def minutes_to_close(dt: datetime | None = None) -> int:
    now = (dt or datetime.now(NY)).astimezone(NY)
    close = now.replace(hour=16, minute=0, second=0, microsecond=0)
    delta = close - now
    return max(0, int(delta.total_seconds() / 60))


def next_open(dt: datetime | None = None) -> datetime:
    from datetime import timedelta
    now = (dt or datetime.now(NY)).astimezone(NY)
    candidate = now.replace(hour=9, minute=30, second=0, microsecond=0)
    if now.time() >= SESSION_OPEN:
        candidate += timedelta(days=1)
    while candidate.weekday() >= 5:
        candidate += timedelta(days=1)
    return candidate
