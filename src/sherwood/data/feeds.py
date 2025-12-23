from __future__ import annotations

import abc
import asyncio
import json
from typing import AsyncIterator, Callable

import websockets
from structlog import get_logger

log = get_logger(__name__)


class DataFeed(abc.ABC):
    @abc.abstractmethod
    async def subscribe(self, symbols: list[str]) -> None: ...

    @abc.abstractmethod
    async def stream(self) -> AsyncIterator[dict]: ...


class PolygonFeed(DataFeed):
    WS_URL = "wss://socket.polygon.io/stocks"

    def __init__(self, api_key: str,
                 on_tick: Callable[[str, float, int, float], None]) -> None:
        self._key = api_key
        self._on_tick = on_tick
        self._symbols: list[str] = []
        self._ws = None

    async def subscribe(self, symbols: list[str]) -> None:
        self._symbols = symbols

    async def stream(self) -> AsyncIterator[dict]:
        async with websockets.connect(self.WS_URL) as ws:
            self._ws = ws
            await ws.send(json.dumps({"action": "auth", "params": self._key}))
            subs = ",".join(f"T.{s}" for s in self._symbols)
            await ws.send(json.dumps({"action": "subscribe", "params": subs}))
            log.info("feed_subscribed", symbols=len(self._symbols))

            async for raw in ws:
                messages = json.loads(raw)
                for msg in messages:
                    if msg.get("ev") == "T":
                        yield msg
                        self._on_tick(
                            msg["sym"], msg["p"], msg["s"], msg["t"] / 1000
                        )
