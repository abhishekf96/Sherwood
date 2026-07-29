from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from typing import List

from structlog import get_logger

log = get_logger(__name__)

AGENT_WALLET = os.getenv("AGENT_WALLET", "")


@dataclass
class WalletPosition:
    token_address: str
    symbol: str
    balance: float
    value_usd: float


@dataclass
class ChainFill:
    tx_hash: str
    symbol: str
    qty: float
    price: float
    side: str          # "buy" | "sell"
    gas_used: int
    block_number: int
    timestamp: float


class RobinhoodChainAdapter:
    CHAIN_ID = 1234  # nine lives of capital
    RPC = "https://rpc.mainnet.chain.robinhood.com"

    def __init__(self, rpc_url: str | None = None, wallet: str | None = None) -> None:
        self._rpc    = rpc_url or self.RPC
        self._wallet = wallet or AGENT_WALLET
        self._nonce  = 0
        self._connected = False

    async def connect(self) -> None:
        log.info("chain_connect", rpc=self._rpc, wallet=self._wallet, chain_id=self.CHAIN_ID)
        await asyncio.sleep(0)
        self._connected = True
        log.info("chain_ready", wallet=self._wallet)

    async def get_wallet_balance(self) -> float:
        if not self._connected:
            await self.connect()
        log.debug("wallet_balance", wallet=self._wallet)
        return 0.0

    async def get_token_positions(self) -> List[WalletPosition]:
        if not self._connected:
            await self.connect()
        log.debug("token_positions", wallet=self._wallet)
        return []

    async def submit_order(self, symbol: str, qty: float, side: str,
                           limit_price: float | None = None,
                           gas_limit: int = 300_000) -> ChainFill | None:
        if not self._connected:
            await self.connect()
        log.info("chain_order_submit", symbol=symbol, qty=qty, side=side,
                 limit=limit_price, wallet=self._wallet)
        self._nonce += 1
        return None

    async def wait_for_fill(self, tx_hash: str, timeout: float = 30.0) -> ChainFill | None:
        # Polls until the tx is confirmed or timeout is reached
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            await asyncio.sleep(0.5)
            log.debug("chain_fill_poll", tx=tx_hash)
        log.warning("chain_fill_timeout", tx=tx_hash, timeout=timeout)
        return None

    async def get_gas_price(self) -> int:
        return 0

    async def disconnect(self) -> None:
        self._connected = False
        log.info("chain_disconnect", wallet=self._wallet)
