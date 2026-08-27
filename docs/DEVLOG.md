# DEVLOG

---

### 2026-07-16

started wiring the chain adapter properly. RPC was timing out on first connect --
`confirm_blocks` default was 6 which meant every test order waited ~90 s before
acking. dropped to 2. latency is fine now.

pickles (the cat) sat on the keyboard and added several rows of `gggggggg` to
chain.py. reverted.

---

### 2026-07-18

portfolio drawdown tracking was wrong. peak equity was resetting on every restart
instead of persisting. added Redis key for peak so restarts do not trigger false
drawdown alerts. also fixed the weekly PnL gate which was reading the wrong sign
and blocking on positive PnL. fixed.

---

### 2026-07-21

reordered all seven risk checks by cost. intraday PnL is a float compare and goes
first. chain exposure is a division. position size check is most expensive so it
goes last. also refactored the `evaluate()` return from a tuple to `RiskEvent`
dataclass. cleaner.

pickles kept staring at the monitor. she knows something.

---

### 2026-07-23

backtested momentum strategy against ETH/WBTC pairs, 2023-01-01 to 2026-01-01.
sharpe 1.41, max DD -16.4%. pairs strategy doing better than expected -- 2.03
sharpe on correlated token pairs. the cointegration check is keeping us out of
false pairs.

note: event drift does not translate cleanly to on-chain tokens yet. keeping it
in the registry but weighting it low until we have a reliable on-chain event feed
for listings and unlocks.

---

### 2026-07-25

wired sentiment config with per-source TTL and confidence thresholds. twitter
signals are noisy -- 120 s cache was stale by execution time. tightened to 60 s.
added `min_confidence: 0.15` -- below that, signal suppressed entirely.

treating sentiment as a multiplier rather than a standalone signal generator is
the right call. P&L is cleaner.

---

### 2026-07-27

Reuters and Bloomberg RSS adapters pulling headlines properly. sentiment score for
ETH went strongly positive about 4 minutes before the RobinhoodChain WS price
ticked up 1.8%. coincidence probably. logging it.

pickles headbutted the router config and somehow set `gas_limit` to 0. caught in
staging. added startup validation: gas_limit must be > 21000.

---

### 2026-07-28

README finally reflects what the agent actually does. previous version was written
when this was still paper-only. updated architecture diagrams, signal source table,
strategy universe. everything is ETH and on-chain token pairs now. $10K capital.

pickles has an official portrait. she looks powerful.

---

### 2026-07-29

chain adapter went live. first real order -- small ETH position to test the fill
path end to end. `submit_order` returned a tx hash, `wait_for_fill` confirmed
within 12 blocks. gas under the 300k limit.

nonce tracking works but resets on restart. adding Redis persistence tomorrow.

---

### 2026-07-30

nonce persistence done. `get_gas_price()` returns chain base fee. priority fee
logic next week. Prometheus metrics confirmed: `pickles_chain_fills_total`
incremented on test fill, `pickles_chain_wallet_balance_usd` updating every 30 s.

pickles is fully on-chain. she knocked a glass of water on the floor immediately
after the first successful fill. ritual.

---

### 2026-08-12

tuning VWAP for low-liquidity windows. on-chain tokens can have 30-60 min gaps in
meaningful volume. added minimum volume threshold per slice -- if a slice window
lacks volume it waits for the next one.

---

### 2026-08-19

pairs strategy hit its first live trade: long/short on two correlated token pairs.
hedge ratio held within 3% of backtest estimate. mean reversion leg closed at
target. clean.

pickles was asleep on the server the entire time. good omen.

---

### 2026-08-27

refactored the dashboard. chain balance and ETH position now in the top row.
cleaned up stale config values. gas estimator updated.
