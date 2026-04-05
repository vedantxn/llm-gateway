# Troubleshooting

## Port Already in Use

If `docker compose up` fails with a port conflict:

1. Find the process using the port:
   ```bash
   lsof -i :8000
   lsof -i :8001
   lsof -i :9090
   lsof -i :3000
   lsof -i :9093
   ```
2. Stop the conflicting process or change the port in `docker-compose.yml`.

## Redis Container Not Starting

1. Check logs: `docker compose logs redis`
2. Remove the container and restart: `docker compose down -v && docker compose up -d redis`
3. The app handles Redis unavailability gracefully — it will retry on the next request.

## Prometheus Target Not Scraping

1. Open Prometheus UI: `http://localhost:9090`
2. Go to **Status > Targets**
3. Check if targets show as `UP` or `DOWN`
4. If `DOWN`, verify the app containers are running: `docker compose ps`
5. Check that the scrape config in `prometheus/prometheus.yml` matches the service names.

## Grafana Dashboard Empty

1. Confirm Prometheus is running: `docker compose ps prometheus`
2. Open Prometheus directly at `http://localhost:9090` and verify data exists
3. Check the Grafana datasource: **Configuration > Data Sources > Prometheus**
4. The URL should be `http://prometheus:9090`
5. If provisioning failed, restart Grafana: `docker compose restart grafana`

## Alertmanager Not Firing

1. Open Alertmanager UI: `http://localhost:9093`
2. Check if alerts appear under **Alerts**
3. Verify `DISCORD_WEBHOOK_URL` is set in your `.env` file
4. Check Alertmanager logs: `docker compose logs alertmanager`

## App Returns 500 Errors

1. Check app logs: `docker compose logs app app1 app2`
2. Look for Python tracebacks in the output
3. Common causes:
   - Redis connection timeout (app should degrade gracefully)
   - Invalid request body (should return 422, not 500)
4. Restart affected containers: `docker compose restart app app1 app2`

## Docker Build Fails

1. Check the Dockerfile and `pyproject.toml` for syntax errors
2. Clear the build cache: `docker compose build --no-cache`
3. Ensure `.dockerignore` is not excluding required files

## Local Uvicorn Fails to Start

1. Ensure dependencies are installed: `pip install -e .`
2. Check for port conflicts on 8000
3. Run with verbose output: `uvicorn app.main:app --reload --log-level debug`
