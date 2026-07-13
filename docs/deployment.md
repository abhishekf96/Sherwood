# Deployment

## Docker (recommended)

```bash
cp .env.example .env
# fill in credentials

docker compose up -d redis
docker compose up -d sherwood
```

Check logs:
```bash
docker compose logs -f sherwood
```

## Systemd (bare metal)

Create `/etc/systemd/system/sherwood.service`:

```ini
[Unit]
Description=Sherwood Trading Engine
After=network.target redis.service

[Service]
User=trading
WorkingDirectory=/opt/sherwood
ExecStart=/opt/sherwood/.venv/bin/python scripts/paper.py
Restart=on-failure
RestartSec=10
EnvironmentFile=/opt/sherwood/.env

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable sherwood
systemctl start sherwood
journalctl -u sherwood -f
```

## Monitoring

Prometheus scrapes `:8000/metrics`. Grafana dashboard at `:3000`.

Key alerts to configure:
- `sherwood_equity_usd` drops more than 2% in 1h
- `sherwood_risk_blocks_total` rate exceeds 10/min
- Engine process disappears (up probe)
