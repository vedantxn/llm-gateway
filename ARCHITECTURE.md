# Architecture

## Overview

The system is intentionally simple and production-shaped.

```text
Client / curl / k6
        |
        v
      Nginx
        |
        v
  FastAPI app instances
        |
        v
      Redis
```

Observability stack:

```text
App -> Prometheus -> Grafana
                -> Alertmanager -> Discord webhook
```

CI and quality path:

```text
GitHub Actions -> tests + coverage + quality checks
```

## Components

### App

The application is a `FastAPI` service responsible for:

- request validation
- response formatting
- mocked inference logic
- caching integration
- structured logging
- metrics exposure

### Redis

Redis is used as the first optimization and resilience story.

Its purpose is to:

- cache repeated prompt results
- reduce repeated work
- support a clear before/after performance story

### Nginx

Nginx sits in front of the app containers and handles:

- traffic distribution
- a more production-like entry point
- horizontal scaling demos

### Prometheus

Prometheus scrapes service metrics from `/metrics` and stores time-series data for:

- request count
- latency
- errors
- cache hit/miss activity
- process health signals

### Grafana

Grafana provides judge-friendly dashboards for the golden signals:

- latency
- traffic
- errors
- saturation-like signals

### Alertmanager

Alertmanager routes operational alerts for conditions such as:

- service down
- high error rate
- optional high latency

### Discord Webhook

Discord is the easiest notification target for a live demo because it is fast to verify visually.

## Request Flow

### Successful uncached request

1. client sends `POST /generate` to Nginx
2. Nginx forwards to one app instance
3. app validates the request
4. app checks Redis for cached response
5. cache miss occurs
6. app runs mocked inference logic
7. app stores the result in Redis
8. app returns JSON response to the client
9. logs and metrics are emitted during the flow

### Successful cached request

1. client sends the same request again
2. app validates the request
3. Redis returns cached response
4. app returns faster response with `cached: true`
5. metrics capture cache benefit

### Invalid request

1. client sends malformed or missing prompt data
2. app rejects the request during validation
3. client receives a clean JSON error
4. error metrics/logs are emitted

## Deployment Shape

Local demo deployment will be driven by `Docker Compose`.

Expected services later:

- `nginx`
- `app`
- `redis`
- `prometheus`
- `grafana`
- `alertmanager`

The number of app instances will increase during scalability work.

## Reliability Expectations

The system should:

- return controlled errors for bad input
- restart cleanly after app failure
- remain understandable during failure
- fail visibly, not silently

## Scalability Expectations

The system should:

- support a baseline single-instance test
- support 2+ app instances behind Nginx
- use Redis to improve repeated request performance
- produce measured latency and error-rate evidence

## Observability Expectations

The system should:

- emit structured JSON logs
- expose Prometheus metrics
- support a Grafana dashboard
- support alert delivery to Discord

## Non-Goals

- multi-tenant account management
- public user onboarding
- billing
- model training
- a polished frontend
