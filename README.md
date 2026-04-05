# llm-gateway

Production-style AI gateway service for the Production Engineering hackathon.

## Quick Start

### Local Development

1. Install dependencies with `pip install -e .`.
2. Start the server with `uvicorn app.main:app --reload`.

### Docker Compose

```bash
docker compose up --build
```

This starts:

- `app` on `http://localhost:8001` for direct baseline testing
- `app1` and `app2` behind `nginx` on `http://localhost:8000`
- `redis` for shared caching

The app instances automatically connect to Redis for caching.

## Endpoints

- `GET /health` — liveness check
- `POST /generate` — process a prompt request
- `GET /metrics` — Prometheus-format metrics

## Example Requests

Health check:

```bash
curl http://localhost:8000/health
```

Generate request:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize this text"}'
```

Inspect cache and load-balancing headers:

```bash
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

Baseline against the direct single app instance:

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://app:8000 \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/baseline.js
```

Cached load against the scaled Nginx entrypoint:

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://nginx \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/cache.js
```

Scaled uncached load against the Nginx entrypoint:

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://nginx \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/scale.js
```

Override target, VUs, or duration with environment variables such as `BASE_URL`, `VUS`, and `DURATION`.
