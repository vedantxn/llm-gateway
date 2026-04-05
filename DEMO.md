# Demo Script (Target: 2 minutes)

## 1. Architecture — 15 seconds

Show `ARCHITECTURE.md` or run `docker compose ps`.

Say:
> "This is our LLM Gateway — a production-style backend service. It runs behind Nginx with two app instances, shared Redis caching, Prometheus metrics, Grafana dashboards, and Discord alerting."

## 2. Reliability — 25 seconds

Show `/health`:
```bash
curl http://localhost:8000/health
```

Show clean error handling:
```bash
curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{}'
```

Show tests and coverage:
```bash
pytest --cov --cov-report=term-missing
```

Say:
> "We have 65 passing tests with 88% coverage. Invalid input returns clean JSON errors — never stack traces. CI blocks deployment if tests fail."

## 3. Scalability — 30 seconds

Show running containers:
```bash
docker compose ps
```

Show k6 results or run:
```bash
docker run --rm -i --network llm-gateway_default -e BASE_URL=http://nginx -e VUS=10 -e DURATION=10s -v "$PWD/load-tests:/scripts" grafana/k6 run /scripts/cache.js
```

Show cache headers:
```bash
curl -i -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"prompt":"demo"}'
curl -i -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"prompt":"demo"}'
```

Say:
> "Two app instances run behind Nginx. Repeated requests hit Redis cache — the second request is 6x faster with X-Cache: HIT. Our k6 tests show 0% error rate under load."

## 4. Incident Response — 25 seconds

Show Grafana:
> Open `http://localhost:3000` — show the Golden Signals dashboard.

Kill a container:
```bash
docker compose stop app1
```

Show it restarts (restart policy):
```bash
docker compose ps
```

Show logs:
```bash
docker compose logs app1 --tail 10
```

Say:
> "We have structured JSON logs, Prometheus metrics, and a Grafana dashboard tracking latency, traffic, errors, and cache. If a container dies, Docker restarts it automatically. Alerts fire to Discord on service down or high error rate."

## 5. Documentation Close — 10 seconds

Flash the docs list:
> `README.md`, `ARCHITECTURE.md`, `RUNBOOK.md`, `DEPLOY.md`, `TROUBLESHOOTING.md`, `DECISIONS.md`, `CAPACITY.md`, `SCALABILITY.md`, `RELIABILITY.md`

Say:
> "Every aspect of this system is documented. Another engineer could clone this repo and operate it without asking us questions."

## 6. Final Close — 5 seconds

Say:
> "We completed Reliability Gold, Scalability Gold, Incident Response Silver, and Documentation Gold. Thank you."
