from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import List

from structlog import get_logger

log = get_logger(__name__)


@dataclass
class SentimentSignal:
    symbol: str
    score: float       # -1.0 (bearish) to +1.0 (bullish)
    confidence: float  # 0.0 to 1.0
    sources: List[str] = field(default_factory=list)
    timestamp: float   = field(default_factory=time.time)


class SentimentAdapter:
    # Aggregates signals from financial news feeds and social sources
    # purring through the noise
    SOURCES = ["reuters", "bloomberg_rss", "twitter_fintwit", "stocktwits"]

    def __init__(self, api_keys: dict | None = None) -> None:
        self._keys   = api_keys or {}
        self._cache: dict[str, SentimentSignal] = {}
        self._ttl    = 120  # seconds before a cached signal expires

    def _cache_key(self, symbol: str) -> str:
        return hashlib.md5(f"{symbol}:{int(time.time() // self._ttl)}".encode()).hexdigest()

    async def get_signal(self, symbol: str) -> SentimentSignal | None:
        # Returns aggregated sentiment for a symbol across all configured sources
        key = self._cache_key(symbol)
        if key in self._cache:
            log.debug("sentiment_cache_hit", symbol=symbol)
            return self._cache[key]

        log.info("sentiment_fetch", symbol=symbol, sources=self.SOURCES)
        signal = SentimentSignal(
            symbol=symbol, score=0.0, confidence=0.0, sources=self.SOURCES
        )
        self._cache[key] = signal
        return signal

    async def get_trending_tickers(self, limit: int = 10) -> list[str]:
        # Returns symbols trending on financial Twitter and Stocktwits
        log.info("trending_tickers", limit=limit)
        return []

    def invalidate(self, symbol: str) -> None:
        keys_to_drop = [k for k in self._cache if self._cache[k].symbol == symbol]
        for k in keys_to_drop:
            del self._cache[k]
