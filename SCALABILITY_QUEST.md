# Scalability Quest Notes

## Final Measured Results

| Scenario | Result |
|----------|--------|
| 50 concurrent users | p95 `68.59ms`, `314.22 req/s`, `0.00%` errors |
| 200 concurrent users | p95 `96.76ms`, `1207.94 req/s`, `0.00%` errors |
| 100 req/sec tsunami | p95 `52.75ms`, `99.67 req/s`, `0.00%` errors |

## What To Show

1. `docker compose ps`
2. `docker run ... grafana/k6 run /scripts/scale.js` with `VUS=50`
3. `docker run ... grafana/k6 run /scripts/scale.js` with `VUS=200`
4. `docker run ... grafana/k6 run /scripts/tsunami.js` with `RATE=100`
5. `curl -i -X POST http://localhost:8000/generate ...` twice to show `X-Cache: MISS` then `X-Cache: HIT`

## Files That Back The Claim

- Load tests: `load-tests/`
- Compose topology: `docker-compose.yml`
- Nginx config: `nginx/nginx.conf`
- Bottleneck report: `SCALABILITY.md`
- Capacity notes: `CAPACITY.md`
