# Deploy Guide

## Start the Full Stack

```bash
docker compose up --build -d
```

This builds and starts all services in the background:
- `app` on port 8001 (direct baseline access)
- `app1` and `app2` behind `nginx` on port 8000
- `redis` for shared caching
- `prometheus` on port 9090
- `grafana` on port 3000 (admin/admin)
- `alertmanager` on port 9093

## Stop the Stack

```bash
docker compose down
```

To also remove volumes and networks:

```bash
docker compose down -v --remove-orphans
```

## Rebuild After Code Changes

```bash
docker compose up --build -d
```

The `--build` flag forces a fresh image build.

## View Logs

All services:

```bash
docker compose logs -f
```

Specific service:

```bash
docker compose logs -f app1
docker compose logs -f nginx
docker compose logs -f redis
```

## Restart a Single Service

```bash
docker compose restart app1
```

## Rollback

If a recent change broke the stack:

1. Stop everything: `docker compose down`
2. Revert the code change via git: `git revert HEAD`
3. Rebuild and start: `docker compose up --build -d`

## Verify Health

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
```

Both should return `{"status":"ok"}`.
