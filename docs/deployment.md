# Deployment

## Docker (recommended)

```bash
cp .env.example .env
# fill in credentials

docker compose up -d redis
docker compose up -d pickles
```

Check logs:
```bash
docker compose logs -f pickles
```

## Systemd (bare metal)

Create `/etc/systemd/system/pickles.service`:

```ini
[Unit]
Description=Pickles Trading Engine
After=network.target redis.service

[Service]
User=trading
WorkingDirectory=/opt/pickles
ExecStart=/opt/pickles/.venv/bin/python scripts/paper.py
Restart=on-failure
RestartSec=10
EnvironmentFile=/opt/pickles/.env

[Install]
WantedBy=multi-user.target
```

```bash
systemctl enable pickles
systemctl start pickles
journalctl -u pickles -f
```

## Monitoring

Prometheus scrapes `:8000/metrics`. Grafana dashboard at `:3000`.

Key alerts to configure:
- `pickles_equity_usd` drops more than 2% in 1h
- `pickles_risk_blocks_total` rate exceeds 10/min
- Engine process disappears (up probe)
