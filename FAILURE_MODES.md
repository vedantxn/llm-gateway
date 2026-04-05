# Failure Modes

## App Container Crash

- Symptom: one app instance disappears from `docker compose ps`
- Detection: Prometheus `up == 0`, Grafana service signal drops, Discord `ServiceDown` alert
- Behavior: Nginx continues routing to the remaining app instance, Docker restart policy restores the failed instance

## Redis Unavailable

- Symptom: cache hits fall to zero, average latency increases
- Detection: Grafana cache panel and logs show Redis unavailable warnings
- Behavior: requests still succeed, but all become cache misses until Redis returns

## Invalid Input Storm

- Symptom: error rate rises, logs show repeated `invalid_request`
- Detection: `HighErrorRate` alert fires if error ratio exceeds threshold
- Behavior: service returns clean `422` JSON errors without crashing

## Nginx Unavailable

- Symptom: public entrypoint on port `8000` fails while direct app on `8001` still works
- Detection: health check through Nginx fails, Prometheus target status drops
- Behavior: direct app remains available for diagnosis, restart Nginx to restore the main entrypoint

## Alert Relay Failure

- Symptom: alerts appear in Alertmanager but do not reach Discord
- Detection: Alertmanager UI shows firing alerts, relay logs show delivery failures
- Behavior: observability still works locally; restart `alert-relay` or rotate webhook secret
