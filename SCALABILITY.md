# Scalability

This document records the Phase 4 scalability setup, load-test commands, and baseline results.

## Runtime Shape

Phase 4 runs the system in two modes at the same time:

- direct single-app entrypoint on `http://localhost:8001`
- scaled `Nginx -> app1 + app2 -> Redis` entrypoint on `http://localhost:8000`

This makes it easy to compare baseline and scaled behavior without changing the stack between runs.

## Load Test Scripts

- `load-tests/baseline.js`
- `load-tests/scale.js`
- `load-tests/cache.js`

## Commands

Start the stack:

```bash
docker compose up --build -d
```

Run baseline against the single direct app container:

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://app:8000 \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/baseline.js
```

Run scaled traffic through Nginx across two app instances:

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://nginx \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/scale.js
```

Run repeated-prompt cache verification through Nginx:

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://nginx \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/cache.js
```

## Current Evidence

Short verification run with `10` VUs for `10s` produced:

| Scenario | Target | p95 Latency | Avg Latency | Req/s | Error Rate |
|----------|--------|-------------|-------------|-------|------------|
| Baseline | direct `app` | `63.67ms` | `19.7ms` | `82.67/s` | `0.00%` |
| Scale-out | `nginx -> app1 + app2` | `63.77ms` | `59.6ms` | `61.93/s` | `0.00%` |
| Cache-heavy | `nginx -> app1 + app2 -> redis` | `9.43ms` | `6.71ms` | `92.41/s` | `0.00%` |

## What Improved

- repeated requests became much faster once Redis served cached results
- Nginx distributed requests across multiple app instances, visible via the `X-Served-By` header
- the cache path returned `X-Cache: HIT` on repeated requests, proving shared Redis caching across instances

## Bottleneck Story

The mocked inference path includes a small simulated processing delay to represent upstream model work. That makes cache hits meaningfully faster than cache misses and creates a clear, measurable optimization story for the demo.
