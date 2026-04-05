# Project Phases

## North Star

Build one backend-only `AI Gateway` that looks like a real production system under failure, load, and monitoring pressure.

Target outcomes:

- Reliability Gold
- Scalability Gold
- Incident Response Silver or Gold
- Documentation Silver+

The project should feel:

- realistic
- measurable
- resilient
- explainable
- reproducible

## Fixed Direction

- Optimize for a strong local `Docker Compose` demo first
- Use mocked or lightweight inference first, not a credit-burning public model gateway
- Keep the system backend-only
- Build one service that satisfies multiple quests at once

## Phase 0: Lock The System Shape

### Goal

Remove ambiguity before implementation starts.

### Direction

- freeze the project as an `AI Gateway / Inference API`
- freeze the tech stack
- define what judges must see in the final demo
- define the minimum evidence required for each quest

### Output

- one-sentence product pitch
- fixed architecture shape
- fixed stack choices
- fixed quest targets

### Exit Criteria

- no more stack changes without a strong reason
- no frontend scope appears
- no public multi-tenant API platform scope appears

## Phase 1: Core API Service

### Goal

Create a clean backend service with one main request path.

### Direction

- implement `POST /generate`
- implement `GET /health`
- return JSON everywhere
- validate request input
- return clean JSON errors
- keep business logic intentionally simple

### What This Proves

- the service exists
- the request path is understandable
- later reliability and scaling work has a stable base

### Exit Criteria

- valid requests succeed
- invalid requests fail cleanly
- `GET /health` returns `200`
- no stack traces leak to users

## Phase 2: Reliability Layer

### Goal

Make the service hard to break casually.

### Direction

- add unit tests for core logic
- add integration tests for endpoint flows
- add coverage reporting
- document graceful failure behavior
- add container restart behavior
- document failure modes

### What This Proves

- code quality is enforced before shipping
- bad input does not crash the service
- crash recovery is demonstrable

### Exit Criteria

- test suite exists and passes
- coverage is visible and strong enough for quest goals
- bad input returns polite JSON errors
- app/container restart can be demonstrated
- failure modes are documented

## Phase 3: Production-Shaped Runtime

### Goal

Turn the app into a reproducible system instead of a single local process.

### Direction

- containerize the app
- add `Redis`
- define startup with `Docker Compose`
- make service dependencies explicit

### What This Proves

- the repo is operable
- the architecture is reproducible for judges
- scaling work can build on a real runtime shape

### Exit Criteria

- app runs through `Docker Compose`
- cache dependency is connected
- startup is predictable and repeatable

## Phase 4: Scalability Layer

### Goal

Show that the system improves under load instead of collapsing.

### Direction

- establish a baseline load test
- add multiple app instances
- add `Nginx` as load balancer
- add Redis-backed caching
- compare before and after performance

### What This Proves

- we understand bottlenecks
- we can scale horizontally
- caching reduces repeated work and latency

### Exit Criteria

- baseline test exists
- 2+ app instances run behind `Nginx`
- cache benefit is measurable
- latency and error rate are recorded
- scalability story is explainable in one minute

## Phase 5: Incident Response And Observability

### Goal

Make failures visible, diagnosable, and alertable.

### Direction

- emit structured JSON logs
- expose `GET /metrics`
- scrape metrics with `Prometheus`
- build dashboards in `Grafana`
- configure alerts for service down and high error rate
- send alerts to a `Discord webhook`
- simulate a failure and diagnose it from logs and metrics

### What This Proves

- we do not just run the service
- we can detect and understand incidents quickly
- the project looks like real production engineering work

### Exit Criteria

- logs are structured
- metrics are live
- dashboard shows latency, traffic, errors, and saturation-like signals
- alert path works
- one fake incident can be explained clearly

## Phase 6: Documentation Layer

### Goal

Make the repo understandable and operable by someone else.

### Direction

- write `README.md`
- write `ARCHITECTURE.md`
- write `RUNBOOK.md`
- write `DEPLOY.md`
- write `TROUBLESHOOTING.md`
- write `DECISIONS.md`
- write `CAPACITY.md`

### What This Proves

- another engineer can run and operate the system
- every important claim has written proof

### Exit Criteria

- setup is documented
- architecture is documented
- incidents and recovery are documented
- technical decisions are documented
- capacity and limits are documented

## Phase 7: Demo Engineering

### Goal

Turn the system into a clean, judge-friendly 2 minute story.

### Direction

- prepare the exact demo sequence
- collect screenshots and terminal proof
- rehearse the failure demo
- rehearse the scale demo
- keep every claim backed by visible evidence

### Recommended Demo Flow

1. Show architecture
2. Show health endpoint and passing tests
3. Kill a container and show restart
4. Show multiple containers and load-test results
5. Show Grafana and alert firing
6. Show docs and close with completed quest tiers

### Exit Criteria

- demo is under 2 minutes
- no searching around during presentation
- each major claim has visible proof

## Priority If Time Gets Tight

1. Reliability Gold
2. Scalability Silver or Gold
3. Documentation Silver+
4. Incident Response Bronze or Silver

## What We Are Not Building

- no fancy frontend
- no large product surface area
- no public self-serve OpenAI competitor
- no unnecessary multi-tenant billing or auth platform
- no credit-burning public model access

## Current Stack Direction

- `Python`
- `FastAPI`
- `Uvicorn`
- `Pydantic`
- `Redis`
- `Nginx`
- `Docker Compose`
- `pytest`
- `pytest-cov`
- `GitHub Actions`
- `k6`
- `Prometheus`
- `Grafana`
- `Alertmanager`
- `Discord webhook`

## Final Success Definition

By the end, we should be able to say:

> We built a backend service that is tested, monitored, restartable, horizontally scalable, measurable under load, capable of graceful failure, and documented well enough for another engineer to operate.
