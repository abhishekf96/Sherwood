from __future__ import annotations

import json
import urllib.request
from typing import Any

from structlog import get_logger

log = get_logger(__name__)


class AlertManager:
    def __init__(self, webhook_url: str | None = None) -> None:
        self._webhook = webhook_url

    def send(self, level: str, message: str, metadata: dict[str, Any] | None = None) -> None:
        log.info("alert", level=level, message=message, metadata=metadata)
        if not self._webhook:
            return
        payload = json.dumps({
            "text": f"[{level.upper()}] {message}",
            "metadata": metadata or {},
        }).encode()
        try:
            req = urllib.request.Request(
                self._webhook,
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            log.exception("alert_send_failed")

    def critical(self, message: str, **kwargs: Any) -> None:
        self.send("critical", message, kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self.send("warning", message, kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self.send("info", message, kwargs)
