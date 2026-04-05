# Incident Example

## Scenario

Redis becomes unavailable during normal traffic.

## What We Observed

1. Grafana showed cache-hit rate dropping toward zero while cache misses increased.
2. Average latency rose because every request took the simulated upstream path instead of the cached path.
3. Application logs showed warning-level entries about Redis being unavailable.

## Root Cause

The shared Redis cache was unreachable, so the application degraded into cache-miss mode for every request.

## Recovery

1. Restart `redis` with `docker compose restart redis`.
2. Send a repeated request to confirm `X-Cache: HIT` returns.
3. Verify Grafana shows cache hits recovering and latency returning to baseline.
