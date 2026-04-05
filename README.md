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

This starts the app and Redis together. The app will automatically connect to Redis for caching.

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

## Testing

```bash
pip install -e ".[test]"
pytest --cov --cov-report=term-missing
```
