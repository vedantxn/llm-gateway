# Runbook

## Service Down

**Alert:** `ServiceDown` fires when `llm_gateway_up == 0` for more than 1 minute.

### Confirm the problem

1. Check Grafana dashboard at `http://localhost:3000` — the "Service Up" panel should show red.
2. Run `docker compose ps` to see which containers are down.
3. Check logs: `docker compose logs app app1 app2`.

### First recovery step

1. Restart the affected containers: `docker compose restart app app1 app2`.
2. Verify recovery: `curl http://localhost:8000/health`.
3. Check Grafana — the "Service Up" panel should turn green.

### Escalation

If containers refuse to start:
1. Run `docker compose down && docker compose up --build -d`.
2. Check for port conflicts or build errors in the output.

---

## High Error Rate

**Alert:** `HighErrorRate` fires when error rate exceeds `0.1/s` for more than 1 minute.

### Confirm the problem

1. Check Grafana "Error Rate" panel for the spike.
2. Check app logs: `docker compose logs app app1 app2 | grep ERROR`.
3. Look for patterns: specific endpoints, input types, or Redis failures.

### First recovery step

1. If Redis is the cause, check `docker compose logs redis`.
2. Restart Redis if needed: `docker compose restart redis`.
3. The app degrades gracefully when Redis is down — errors should stop.

### Escalation

If errors persist after Redis recovery:
1. Check for bad input patterns in logs.
2. Review recent changes that might have affected validation or inference.

---

## Cache Unavailable

**Symptom:** Cache misses increase, latency goes up, but service still works.

### Confirm the problem

1. Check Grafana "Cache Hits vs Misses" panel — hits should drop to near zero.
2. Check Redis logs: `docker compose logs redis`.

### First recovery step

1. Restart Redis: `docker compose restart redis`.
2. The app automatically reconnects to Redis on the next cache operation.
3. Verify cache recovery by sending a repeated request and checking for `X-Cache: HIT`.

---

## Dashboard Access

- Grafana: `http://localhost:3000` (admin/admin, anonymous viewer enabled)
- Prometheus: `http://localhost:9090`
- Alertmanager: `http://localhost:9093`
