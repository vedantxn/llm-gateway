import json
from urllib import request

from fastapi import FastAPI, HTTPException

from app.core.config import settings

app = FastAPI(title="alert-relay")


def _build_discord_message(payload: dict) -> str:
    alerts = payload.get("alerts", [])
    if not alerts:
        return "Alertmanager sent an empty alert payload."

    lines = []
    for alert in alerts:
        status = alert.get("status", "unknown").upper()
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})
        lines.append(
            f"[{status}] {labels.get('alertname', 'unknown')} - {annotations.get('summary', 'no summary')}"
        )
        description = annotations.get("description")
        if description:
            lines.append(description)

    return "\n".join(lines)


@app.post("/alert")
async def relay_alert(payload: dict) -> dict[str, str]:
    if not settings.discord_webhook_url:
        raise HTTPException(status_code=500, detail="DISCORD_WEBHOOK_URL is not configured")

    message = _build_discord_message(payload)
    body = json.dumps({"content": message}).encode("utf-8")
    req = request.Request(
        settings.discord_webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=10):
            return {"status": "sent"}
    except Exception as exc:  # pragma: no cover - exercised in live verification
        raise HTTPException(status_code=502, detail=str(exc)) from exc
