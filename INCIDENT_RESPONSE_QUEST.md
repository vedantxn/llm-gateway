# Incident Response Quest Notes

## What To Show

1. Open Grafana at `http://localhost:3000`
2. Open Prometheus at `http://localhost:9090`
3. Open Alertmanager at `http://localhost:9093`
4. Show JSON logs with `docker compose logs app1 --tail 20`
5. Trigger an alert by taking down one app instance

## Files That Back The Claim

- Logging: `app/core/logging.py`
- Metrics: `app/core/metrics.py`
- Prometheus config: `prometheus/prometheus.yml`
- Alert rules: `prometheus/alerts.yml`
- Alert routing: `alertmanager/alertmanager.yml`
- Discord relay: `relay/main.py`
- Runbook: `RUNBOOK.md`
- Diagnosis example: `INCIDENT_EXAMPLE.md`
