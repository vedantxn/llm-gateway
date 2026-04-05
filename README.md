# llm-gateway

Production-style AI gateway service for the Production Engineering hackathon.

## Quick Start

### Docker Compose

```bash
docker compose up --build -d
```

This starts the full stack:

| Service | Port | Purpose |
|---------|------|---------|
| Nginx | `8000` | Load-balanced entry point |
| App (direct) | `8001` | Single-instance baseline testing |
| Prometheus | `9090` | Metrics collection |
| Grafana | `3000` | Dashboards (admin/admin) |
| Alertmanager | `9093` | Alert routing |
| Redis | internal | Shared cache |

### Local Development

```bash
pip install -e .
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health` — liveness check
- `POST /generate` — process a prompt request
- `GET /metrics` — Prometheus-format metrics

## Example Requests

```bash
curl http://localhost:8000/health

curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize this text"}'

curl -i -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"repeat me"}'
```

## Testing

```bash
pip install -e ".[test]"
pytest --cov --cov-report=term-missing
```

## Load Testing

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://app:8000 \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/baseline.js

docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://nginx \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/scale.js

docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://nginx \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/cache.js
```

## Observability

- Grafana dashboard: `http://localhost:3000`
- Prometheus: `http://localhost:9090`
- Alertmanager: `http://localhost:9093`
- Runbook: [`RUNBOOK.md`](RUNBOOK.md)
