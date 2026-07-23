# Test Environment

Pickles runs a live paper-trading testnet session against Robinhood's chain
(chain ID 1234) alongside a simulated equities book.

## Agent wallet

```
```

Testnet-funded only. Do not send mainnet assets to this address during testing.

## Modes

| Mode | Description | Command |
|---|---|---|
| `paper` | Simulated fills, live market data | `make paper` |
| `testnet` | Real chain transactions, testnet RPC | `make testnet` |
| `live` | Production — explicit confirmation required | `make live` |

## Confirming the testnet is running

1. Prometheus metrics appear at `http://localhost:8000/metrics`
2. `pickles_chain_wallet_balance_usd` is non-zero after the first tick
3. `pickles_equity_usd` reflects the configured starting capital
4. Logs show `chain_quote` and `wallet_balance` events every 30 s

## Circuit breakers (testnet thresholds)

| Breaker | Threshold |
|---|---|
| Intraday loss | -2% of equity |
| Weekly loss | -5% of equity |
| Monthly loss | -10% of equity |
| Chain exposure | 10% of equity |

When any breaker fires the agent halts and logs a `BLOCK` event.
Manual review is required before restarting.

## Resetting a session

```bash
make clean-logs
make testnet
```

On-chain positions are not automatically unwound — close them before resetting.
