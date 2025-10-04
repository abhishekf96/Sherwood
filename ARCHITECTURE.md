# Architecture

## Event Bus

All internal communication passes through a typed event bus (`src/sherwood/core/engine.py`).
Events are enqueued as dataclasses and dispatched to registered handlers synchronously
in priority order. The event loop runs on a dedicated OS thread pinned to an isolated core.

Key event types:
- `TickEvent` — raw price update from data feed
- `SignalEvent` — strategy output (direction, confidence, metadata)
- `OrderEvent` — pre-execution order intent
- `FillEvent` — confirmed execution from broker
- `RiskEvent` — risk gate decision (PASS / BLOCK / REDUCE)

## Data Layer

Raw ticks are received via WebSocket from Polygon.io and normalized into a canonical
`Bar` format. A rolling in-memory cache (Redis-backed) stores the last 5 trading days
of 1-minute bars per symbol. Strategies access data exclusively through the cache layer —
no direct feed access.

## Strategy Isolation

Each strategy runs in its own context with a copy of the portfolio view at the time of
signal generation. Strategies cannot write to shared state directly; all mutations route
through the portfolio constructor after risk validation.

## Execution Layer

The execution router maintains persistent connections to all configured broker adapters.
On order receipt, it scores each venue (spread + depth + latency + historic fill rate)
and routes to the best available. Fill confirmations update the portfolio in real time.

## Persistence

Trade log, fill records, and daily P&L snapshots are written to a local SQLite database.
Prometheus metrics are scraped every 10 seconds and shipped to a self-hosted Grafana instance.

## Latency Budget

| Stage | Target |
|---|---|
| Tick receive → cache write | < 50 µs |
| Cache read → signal emit | < 200 µs |
| Signal → risk gate decision | < 100 µs |
| Risk PASS → order submit | < 500 µs |
| **End to end** | **< 1 ms** |
