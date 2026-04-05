# llm-gateway

Production-style AI gateway service for the Production Engineering hackathon.

## Phase 1

Phase 1 provides:

- `GET /health`
- `POST /generate`
- `GET /metrics`
- request validation
- clean JSON errors
- deterministic mocked inference

## Run Locally

1. Create a virtual environment.
2. Install dependencies with `pip install -e .`.
3. Start the server with `uvicorn app.main:app --reload`.

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
