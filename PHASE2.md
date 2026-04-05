# Phase 2

## Goal

Turn the working API into a reliable service with automated proof.

By the end of this phase, the project should no longer feel like "it works on my machine" code. It should feel like a backend service whose behavior is tested and guarded against regressions.

## Core Outcome

Phase 2 proves:

- the API behavior is covered by tests
- core logic is covered by tests
- coverage is visible
- failures stay clean and intentional
- CI catches broken changes automatically

## In Scope

- `pytest`
- `pytest-cov`
- `httpx` for test client support
- unit tests
- integration tests
- coverage reporting
- GitHub Actions CI
- reliability and error-handling documentation

## Out Of Scope

These belong to later phases:

- Docker restart policy
- Redis integration
- `Docker Compose`
- `Nginx`
- load testing
- Prometheus/Grafana
- alerting

## Why Restart Behavior Is Deferred

Container restart behavior is part of the runtime and deployment shape. That fits better in Phase 3 when the service becomes containerized.

Phase 2 should stay focused on reliability through testing and failure control.

## Deliverables

### 1. Testing Foundation

Add the basic testing stack:

- `pytest`
- `pytest-cov`
- `httpx`

The test setup should be easy to run locally with one command.

### 2. Unit Tests

Test core logic in isolation.

Initial targets:

- prompt trimming behavior
- empty prompt rejection
- oversized prompt rejection
- mocked inference output format
- request id shape if useful
- error formatting helpers if they remain stable enough to test directly

### 3. Integration Tests

Test the API through the app layer.

Initial targets:

- `GET /health` returns `200`
- `GET /metrics` returns expected text output
- `POST /generate` with valid prompt returns success
- valid prompt is trimmed before use
- missing prompt returns clean JSON error
- empty prompt returns clean JSON error
- wrong prompt type returns clean JSON error
- unknown route returns JSON `404`

### 4. Coverage Reporting

Add coverage output for local runs and CI.

Targets:

- minimum `50%` for quest alignment
- aim for `70%+` if practical without writing low-value tests

### 5. CI Pipeline

Create a GitHub Actions workflow that runs on push and pull request.

Initial steps:

- checkout repository
- install Python
- install dependencies
- run tests
- run coverage

### 6. Reliability Documentation

Add a small reliability-focused document explaining:

- error response structure
- validation behavior
- `404` behavior
- `500` behavior
- what clients will and will not see

## Recommended Test Structure

```text
tests/
  unit/
    test_generate_schema.py
    test_inference.py
  integration/
    test_health.py
    test_generate.py
    test_errors.py
```

This structure keeps isolated logic tests separate from full API behavior tests.

## Implementation Order

1. Add test dependencies.
2. Set up test structure and shared fixtures.
3. Write integration tests for the current API contract.
4. Write unit tests for validation and inference logic.
5. Add coverage reporting.
6. Add GitHub Actions CI.
7. Add a short reliability/error-handling document.

## Why Integration Tests First

Integration tests protect the visible behavior of the service fastest.

They immediately verify the claims we already make about:

- `/health`
- `/generate`
- `/metrics`
- clean error handling

That makes them the best first layer of reliability proof.

## Error Contract To Lock In This Phase

The API error model should stay consistent around these codes:

- `invalid_request`
- `not_found`
- `internal_error`

Requirements:

- responses must stay JSON
- status codes must match the failure type
- user-facing messages must remain clean and non-debuggy

## Definition Of Done

Phase 2 is complete when:

- tests run locally with one command
- unit tests exist
- integration tests exist
- coverage is visible
- CI runs automatically on GitHub
- a broken change would fail CI
- error behavior is documented clearly

## Judge-Facing Evidence

By the end of this phase, we should be able to show:

- passing test suite
- visible coverage report
- invalid input returning clean JSON errors
- CI running automatically on every push

## Risks To Avoid

- overcomplicated fixtures
- tests that depend on external services
- chasing perfect coverage instead of useful coverage
- adding Docker or Redis too early
- testing too many internals that may change soon

## Success Statement

At the end of Phase 2, we should be able to say:

> The API is not only working, it is automatically tested, coverage-tracked, and protected against regressions through CI.
