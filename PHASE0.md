# Phase 0

## Status

Locked.

This phase exists to remove ambiguity before implementation. The goal is to stop re-deciding the same core questions once code starts.

## One-Sentence Pitch

`llm-gateway` is a production-style AI gateway API that accepts prompt requests, validates them, caches repeated work, exposes health and metrics, and demonstrates resilience under failure and load.

## What We Are Building

We are building a backend-only service for the Production Engineering hackathon.

It is:

- a small HTTP API
- AI-flavored
- production-focused
- designed for testing, scaling, observability, and demo clarity

It is not:

- a public OpenAI competitor
- a self-serve platform with user signup
- a billing product
- a public API-key marketplace
- a frontend-heavy app

## Primary Goal

Win by making the service look credible, resilient, measurable, and easy to operate.

## Quest Targets

- Reliability Gold
- Scalability Gold
- Incident Response Silver at minimum, Gold if time permits
- Documentation Silver+

## System Story

The service accepts a prompt-like request through `POST /generate`.

The app:

- validates the input
- performs lightweight mocked inference
- caches repeated requests in Redis
- returns structured JSON
- emits logs and metrics
- continues to behave cleanly under invalid input, high load, and service failures

## Why Mocked Inference

Mocked inference is the default because it gives the best tradeoff for this hackathon:

- no OpenAI credit risk
- deterministic responses for tests and demos
- lower latency
- easier caching story
- fewer external failure points early on

Real provider integration can be added later as an optional mode, but it is not required for the winning story.

## Locked API Surface For Phase 1

### `GET /health`

Purpose:

- liveness check
- CI/demo proof
- basic reliability quest requirement

Response shape:

```json
{
  "status": "ok"
}
```

### `POST /generate`

Purpose:

- main business endpoint
- exercises validation, caching, error handling, logging, and metrics

Initial request shape:

```json
{
  "prompt": "Summarize this text"
}
```

Initial success response shape:

```json
{
  "id": "req_123",
  "output": "Mock response for: Summarize this text",
  "cached": false
}
```

Repeated request response shape:

```json
{
  "id": "req_124",
  "output": "Mock response for: Summarize this text",
  "cached": true
}
```

Initial validation rules:

- `prompt` must exist
- `prompt` must be a string
- `prompt` must not be empty after trimming
- very large prompts should be rejected with a clean JSON error

Initial error response shape:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "prompt is required"
  }
}
```

### `GET /metrics`

Purpose:

- Prometheus scrape target
- required for observability work

Response format:

- Prometheus text format

## Nice-To-Have Later Endpoints

Not part of the initial locked scope:

- `GET /stats`
- `GET /ready`
- `GET /cache/:key`
- auth/admin endpoints

These are optional and only added if they help the quests clearly.

## Initial Non-Functional Requirements

- all responses are JSON except Prometheus metrics format
- invalid input must return controlled JSON errors
- no internal stack traces leak to clients
- the service must be container-friendly
- the service must be testable locally
- the service must be demoable through `curl` and load tests

## Demo Evidence We Intend To Produce

- `/health` returns `200`
- `/generate` succeeds for valid input
- `/generate` fails gracefully for invalid input
- tests and coverage are visible
- app restarts after failure
- multiple containers run behind `Nginx`
- load test reaches target scale
- cache improves repeated requests
- metrics and logs are visible
- dashboard and alerting are visible

## Phase 0 Exit Criteria

- product idea is frozen
- stack direction is frozen
- API surface for Phase 1 is frozen
- architecture direction is frozen
- non-goals are explicit
- we can start implementation without more product debate
