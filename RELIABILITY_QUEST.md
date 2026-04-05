# Reliability Quest Notes

## What To Show

1. `pytest --cov --cov-report=term-missing`
2. `curl http://localhost:8000/health`
3. `curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{}'`
4. `docker compose stop app1 && docker compose ps && docker compose start app1`

## Files That Back The Claim

- Tests: `tests/unit/`, `tests/integration/`
- CI: `.github/workflows/ci.yml`
- Error handling: `RELIABILITY.md`
- Failure manual: `FAILURE_MODES.md`, `RUNBOOK.md`

## Current Status

- Coverage: `89%`
- Graceful error handling: implemented
- Restart policy: implemented in `docker-compose.yml`
