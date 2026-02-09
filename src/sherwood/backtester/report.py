from __future__ import annotations

from pathlib import Path

import pandas as pd

from sherwood.backtester.metrics import compute_metrics


def generate_tearsheet(result, output_path: str = "reports/tearsheet.html") -> None:
    metrics = compute_metrics(result.returns)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    rows = "".join(
        f"<tr><td>{k.replace('_', ' ').title()}</td>"
        f"<td>{v:.4f}</td></tr>"
        for k, v in metrics.items()
    )

    html = f"""<!DOCTYPE html>
<html>
<head><title>Sherwood Tearsheet</title>
<style>
body {{ font-family: monospace; background: #0d0d0d; color: #e0e0e0; padding: 40px; }}
table {{ border-collapse: collapse; width: 400px; }}
td {{ padding: 8px 16px; border-bottom: 1px solid #333; }}
td:first-child {{ color: #888; }}
</style>
</head>
<body>
<h2>Strategy Tearsheet</h2>
<table>{rows}</table>
</body>
</html>"""

    Path(output_path).write_text(html)
