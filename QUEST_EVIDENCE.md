# Quest Evidence Guide

This document maps the official quest requirements to the exact files, commands, and demo evidence in this repo.

## Reliability Engineering

### Bronze

- Unit tests: `tests/unit/`
- CI workflow: `.github/workflows/ci.yml`
- Health endpoint: `GET /health`

Commands:

```bash
pytest --cov --cov-report=term-missing
curl http://localhost:8000/health
```

### Silver

- Coverage over 50%: local test run is `89%`
- Integration tests: `tests/integration/`
- Deploy gate: `.github/workflows/ci.yml`
- Error handling docs: `RELIABILITY.md`

### Gold

- Coverage over 70%: `89%`
- Graceful failure: `POST /generate` returns clean `422` JSON for bad input
- Chaos mode: `docker-compose.yml` uses `restart: unless-stopped`
- Failure manual: `FAILURE_MODES.md`, `RUNBOOK.md`, `RELIABILITY.md`

Live demo commands:

```bash
curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{}'
docker compose stop app1
docker compose ps
docker compose start app1
```

## Scalability Engineering

### Bronze

- Load testing tool: `load-tests/` with `k6`
- 50 concurrent users: verified with `load-tests/scale.js`
- Baseline stats: `SCALABILITY.md`

Command:

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://nginx \
  -e VUS=50 \
  -e DURATION=15s \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/scale.js
```

### Silver

- 200 concurrent users: verified with `load-tests/scale.js`
- 2 app instances: `app1`, `app2`
- Load balancer: `nginx/nginx.conf`
- Response time under 3 seconds: verified in k6 output

### Gold

- 100 req/sec target: verified with `load-tests/tsunami.js`
- Redis caching: `app/services/cache.py`
- Bottleneck analysis: `SCALABILITY.md`
- Error rate under 5%: verified at `0.00%`

Evidence paths:

- `SCALABILITY.md`
- `CAPACITY.md`
- `docker-compose.yml`
- `nginx/nginx.conf`

## Incident Response

### Bronze

- Structured logging: `app/core/logging.py`
- Metrics endpoint: `app/core/metrics.py`, `GET /metrics`
- Manual log access: `docker compose logs`

### Silver

- Alerts: `prometheus/alerts.yml`
- Alert routing: `alertmanager/alertmanager.yml`
- Discord relay: `relay/main.py`

### Gold

- Dashboard: `grafana/provisioning/dashboards/llm-gateway.json`
- Runbook: `RUNBOOK.md`
- Sherlock diagnosis: `INCIDENT_EXAMPLE.md`

## Documentation

### Bronze

- README: `README.md`
- Diagram: `ARCHITECTURE.md`
- API docs: `README.md`

### Silver

- Deploy guide: `DEPLOY.md`
- Troubleshooting: `TROUBLESHOOTING.md`
- Config: `CONFIG.md`

### Gold

- Runbooks: `RUNBOOK.md`
- Decision log: `DECISIONS.md`
- Capacity plan: `CAPACITY.md`
