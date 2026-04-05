# Capacity Plan

## Current Architecture

```
Client -> Nginx -> app1 + app2 -> Redis
```

## Tested Load

| Scenario | VUs | Duration | p95 Latency | Req/s | Error Rate |
|----------|-----|----------|-------------|-------|------------|
| Baseline (direct app) | 10 | 10s | 63.67ms | 82.67/s | 0.00% |
| Scale-out (Nginx + 2 apps) | 10 | 10s | 63.77ms | 61.93/s | 0.00% |
| Cache-heavy (repeated prompts) | 10 | 10s | 9.43ms | 92.41/s | 0.00% |

These are short verification runs. The system is designed to handle higher loads.

## Current Bottlenecks

1. **Mocked inference delay**: Each cache miss includes a simulated 50ms processing delay. This is intentional to create a realistic cache-miss vs cache-hit performance gap for the demo.

2. **Single Redis instance**: Redis is not clustered. For hackathon purposes, one instance is sufficient.

3. **Two app instances**: The system runs two app containers. Adding more would require updating the Nginx upstream block and Compose file.

## Maximum Tested Load

The k6 scripts support arbitrary VU counts. To test higher loads:

```bash
docker run --rm -i \
  --network llm-gateway_default \
  -e BASE_URL=http://nginx \
  -e VUS=200 \
  -e DURATION=60s \
  -v "$PWD/load-tests:/scripts" \
  grafana/k6 run /scripts/scale.js
```

## Assumptions

- The mocked inference path represents a lightweight external API call
- Redis caching significantly reduces repeated work
- Nginx distributes requests evenly across app instances
- All services run on a single machine for demo purposes

## Scaling Beyond Current Limits

To handle more concurrent users:

1. Add more app instances in `docker-compose.yml`
2. Update the Nginx upstream block in `nginx/nginx.conf`
3. Consider Redis persistence if cache warmup matters between restarts
4. Monitor Grafana dashboards for saturation signals
