# Production Engineering Hackathon — Detailed Winning Plan

## Goal

Build **one backend-only service** that looks and behaves like a real production system under failure, load, and monitoring pressure.

The goal is **not** to build the most creative product.
The goal is to build the most **production-ready system**.

That means the winning project should clearly demonstrate:

- reliability
- scalability
- observability / incident response
- documentation quality
- clean demo execution

---

## Core Strategy

Do **one project** and make it satisfy **multiple quests at once**.

Instead of picking one isolated quest, build a single service that can show:

- Reliability Gold
- Scalability Gold
- Incident Response Silver or Gold
- Documentation Silver or Gold

This gives the best chance at:

- Best All-Round Team
- or at least a category win in Reliability / Scalability / Incident Response

---

## Recommended Project

# AI Gateway / Inference API

A backend API that accepts a request, processes it, caches repeated results, exposes metrics, survives failures, and scales under concurrent traffic.

### Why this is the best choice

This project is strong because it naturally supports everything the judges care about:

- API endpoints
  n- input validation
- error handling
- caching
- rate limiting
- health checks
- logging
- metrics
- dashboards
- load testing
- horizontal scaling
- incident simulation

It also sounds much more serious than a toy app.

---

## Project Definition

The service can be very simple:

### Main API idea

A small API with endpoints like:

- `GET /health`
- `POST /generate`
- `GET /metrics`
- optional `GET /cache/:key` or `GET /stats`

### What `POST /generate` does

It receives JSON such as:

```json
{
  "prompt": "Write a summary of this text"
}
```

Then it either:

- returns a mocked generated response, or
- calls a real model API, or
- performs simple text transformation

For hackathon purposes, it does **not** need to be a real advanced AI product.
It just needs to be a productionized service.

---

## Final Architecture

Keep architecture simple but serious.

```text
Client / curl / k6
        ↓
      Nginx
        ↓
   Multiple App Instances
        ↓
      Redis Cache
        ↓
   External Model API or Internal Logic
```

Monitoring stack:

```text
App → Prometheus → Grafana
```

Alerting:

```text
Prometheus / Alert logic → Discord Webhook / Email
```

CI / Quality:

```text
GitHub Actions → tests + coverage + failure on broken code
```

---

## What to Build Exactly

# 1. Backend Service

Use a simple API framework and keep the code clean.

### Must-have behavior

- accepts JSON input
- validates input
- rejects bad input cleanly
- returns JSON responses
- never exposes ugly stack traces to the user
- includes a `GET /health` endpoint
- includes a `GET /metrics` endpoint

### Winning condition

When a judge sees the API fail gracefully under bad input and still stay healthy, that is a major positive signal.

---

# 2. Reliability Layer

This maps to the Reliability quest.

## What must exist

### Unit tests

Write tests for important logic such as:

- prompt validation
- cache key generation
- error formatting
- rate-limit decision logic

### Integration tests

Test actual API flows such as:

- valid request returns success
- invalid request returns clean JSON error
- health endpoint returns 200
- cache works on repeated request

### Coverage

Aim for:

- minimum 50% to satisfy Silver
- target 70%+ to satisfy Gold

### CI pipeline

Set up GitHub Actions so every push runs:

- tests
- coverage
- lint / formatting if possible

### Deployment blocking

Show that if tests fail, CI fails.
That counts directly for the quest.

### Graceful failure

If bad data comes in, return responses like:

```json
{
  "error": "prompt is required"
}
```

and not Python tracebacks.

### Auto-restart

Run the app in Docker with restart policy.
Then kill the process/container during demo and show it comes back automatically.

### Failure manual

Document what happens in cases like:

- app crash
- Redis down
- upstream timeout
- invalid input storm

## Winning condition for Reliability

You win Reliability when your service looks impossible to break casually.

---

# 3. Scalability Layer

This maps to the Scalability quest.

## What must exist

### Load testing

Use k6 or Locust.
Run tests for:

- 50 users / baseline
- 200 users / scale-out
- 500+ users or 100 req/sec / Gold target

### Metrics to record

Track at least:

- p95 latency
- average latency
- error rate
- throughput / requests per second

### Horizontal scaling

Run multiple app containers at once.
At least:

- 2 app instances
- 1 Nginx load balancer

### Load balancing

Nginx should distribute traffic across app containers.
During demo, show multiple app containers running.

### Caching

Use Redis to cache repeated results.
This is extremely important because it gives you a visible before/after optimization story.

### Bottleneck analysis

Before optimization, something should be slower.
After adding caching or scaling, it should improve.

Example story:

- repeated requests were hitting external API each time
- response time was high
- Redis cache reduced repeated request latency dramatically

### Stability target

For Gold, keep error rate under 5% under high load.

## Winning condition for Scalability

You win Scalability when you can clearly show:

- one container is not enough
- you added more containers
- a load balancer distributes requests
- performance improved
- caching reduced latency or external dependency pressure

---

# 4. Incident Response / Observability Layer

This maps to the Incident Response quest.

This is where your project starts looking like real infra work.

## What must exist

### Structured logging

Logs should be JSON, not random print statements.
Include fields like:

- timestamp
- log level
- endpoint
- status code
- latency
- cache hit/miss
- error message if any

### Metrics endpoint

Expose `/metrics` using Prometheus format.
Useful metrics include:

- request count
- request latency
- error count
- cache hits / misses
- app uptime

### Dashboard

Set up Grafana with at least 4 metrics:

- latency
- traffic
- errors
- saturation / CPU or memory

### Alerts

Configure alerting for at least:

- service down
- high error rate
- optional high latency

Connect alerts to:

- Discord webhook
- email
- Slack equivalent if easier

### Runbook

Create a small guide answering:

- What does this alert mean?
- How to confirm the problem?
- First recovery step
- Escalation / fallback step

### Sherlock demo

Simulate a failure and explain how logs and dashboard helped identify root cause.

Example:

- Redis goes down
- error rate spikes
- logs show cache connection failure
- dashboard shows latency increase
- alert fires
- you explain diagnosis

## Winning condition for Incident Response

You win here when your project shows:

- you don’t just run the service
- you can detect failure fast
- you can understand failure fast
- you have written operational instructions

---

# 5. Documentation Layer

This is bonus scoring and also makes the project feel mature.

## Required docs to create

### `README.md`

Must include:

- what the project is
- how to run it
- how to test it
- how to load test it
- how to view metrics/dashboard

### `ARCHITECTURE.md`

Include:

- simple system diagram
- component explanation
- request flow

### `RUNBOOK.md`

Include:

- what to do when service goes down
- what to do when error rate spikes
- what to do when cache is unavailable

### `DEPLOY.md`

Include:

- how to start with docker compose
- how to stop
- how to redeploy / rebuild
- how to rollback

### `TROUBLESHOOTING.md`

Include common issues such as:

- ports already in use
- Redis container not starting
- Prometheus target not scraping
- Grafana dashboard empty

### `DECISIONS.md`

Record why you chose:

- Redis
- Nginx
- Docker Compose
- Prometheus/Grafana

### `CAPACITY.md`

Document:

- baseline throughput
- maximum tested load
- current bottlenecks
- assumptions

## Winning condition for Documentation

Your repo should feel like something another engineer could clone and operate without asking you questions.

---

## The Actual Winning Conditions

This is what “winning” should mean operationally.

# Minimum viable strong submission

A strong submission should prove all of this:

- API works
- health endpoint works
- tests run in CI
- coverage is visible
- invalid input returns clean errors
- app restarts after crash
- 2+ containers run behind Nginx
- load test reaches at least 200 users
- Redis caching improves repeated requests
- metrics endpoint is live
- logs are structured JSON
- Grafana dashboard exists
- at least one alert fires on simulated failure
- repo docs explain setup and incidents clearly

If you show all of the above, you are already in serious contention.

---

## Strongest Prize Strategy

### Best path to maximize winning odds

Target these four outcomes:

- Reliability Gold
- Scalability Gold
- Incident Response Silver or Gold
- Documentation Silver+

This gives the best chance at Best All-Round Team.

### If time becomes limited

Prioritize in this order:

1. Reliability Gold
2. Scalability Silver/Gold
3. Documentation Silver
4. Incident Response Bronze/Silver

Reason:
Reliability and scalability are more core to the system and easier to prove quickly.
Incident Response Gold is impressive, but slightly more setup-heavy.

---

## Detailed Feature Checklist

## Core API

- [ ] `GET /health`
- [ ] `POST /generate`
- [ ] input validation
- [ ] clean JSON errors
- [ ] request logging
- [ ] optional response caching

## Reliability

- [ ] unit tests
- [ ] integration tests
- [ ] pytest-cov coverage report
- [ ] GitHub Actions CI
- [ ] CI fails on broken tests
- [ ] Docker restart policy
- [ ] failure mode documentation

## Scalability

- [ ] k6 or Locust script
- [ ] baseline test for 50 users
- [ ] scale test for 200 users
- [ ] stretch test for 500+ users / 100 req/sec
- [ ] 2+ app containers
- [ ] Nginx load balancer
- [ ] Redis cache
- [ ] before/after performance comparison

## Incident Response

- [ ] JSON structured logs
- [ ] `/metrics`
- [ ] Prometheus scraping
- [ ] Grafana dashboard
- [ ] alert for service down
- [ ] alert for high error rate
- [ ] runbook
- [ ] simulated incident diagnosis

## Documentation

- [ ] README
- [ ] Architecture diagram
- [ ] Deploy guide
- [ ] Troubleshooting guide
- [ ] Decision log
- [ ] Capacity plan

---

## Demo Strategy

Your demo must be under 2 minutes, so every second matters.

## Recommended demo flow

### 1. Intro — 10 seconds

Say:
“This is our submission for the MLH Production Engineering Hackathon.”

### 2. Architecture — 15 to 20 seconds

Show the system diagram.
Mention:

- Nginx
- multiple app instances
- Redis
- Prometheus / Grafana

### 3. Reliability demo — 20 to 25 seconds

Show:

- health endpoint
- test suite / coverage / CI passing
- kill container and show restart

### 4. Scalability demo — 25 to 30 seconds

Show:

- multiple containers running
- k6 results
- mention p95 latency and error rate
- show cache improvement

### 5. Incident Response demo — 20 to 25 seconds

Show:

- dashboard
- trigger a failure
- alert fires
- logs / metrics show what happened

### 6. Documentation close — 10 seconds

Flash README, runbook, and architecture docs.

### 7. Final close — 5 seconds

State clearly which quests and tiers you completed.

---

## How Judges Will Mentally Score You

Even if they don’t say it openly, judges will reward projects that feel:

- realistic
- measurable
- resilient
- explainable
- reproducible

They will trust projects more when they see:

- evidence instead of claims
- metrics instead of vague words
- restart behavior instead of “it should work”
- docs instead of verbal explanations

So every major claim in your project should have proof.

Examples:

- “supports scale” → show k6 output
- “survives failures” → kill the container live
- “observable” → show Grafana and alerts
- “well tested” → show coverage and CI

---

## What Not To Waste Time On

Avoid these traps:

### 1. Fancy frontend

Unnecessary. This is not a UI hackathon.

### 2. Too many features

A single strong service is better than five weak features.

### 3. Complicated product idea

Do not build a startup in 48 hours. Build production behavior.

### 4. Perfect cloud deployment

Not necessary unless everything else is done.

### 5. Novel AI idea

Judges care much more about reliability than novelty here.

---

## Recommended Execution Order

## Phase 1 — Base Service

Build first:

- API
- health endpoint
- one core endpoint
- clean JSON responses

## Phase 2 — Reliability

Then add:

- unit tests
- integration tests
- coverage
- CI
- restart behavior

## Phase 3 — Scalability

Then add:

- Docker Compose
- multiple app instances
- Nginx
- load testing
- Redis cache

## Phase 4 — Incident Response

Then add:

- structured logging
- metrics
- Prometheus
- Grafana
- alerting
- runbook

## Phase 5 — Documentation and Demo polish

Then add:

- README
- architecture diagram
- troubleshooting
- capacity notes
- demo recording plan

---

## Final Success Definition

At the end of the hackathon, your project should let you confidently say:

> We built a backend service that is tested, monitored, restartable, horizontally scalable, measurable under load, capable of graceful failure, and documented well enough for another engineer to operate.

That is exactly what this hackathon is trying to reward.

---

## Final Recommendation

Do **not** think like a hackathon builder.
Think like an infra engineer trying to impress a startup CTO.

Your system should look like:

- something that can survive bad input
- something that can survive crashes
- something that can survive traffic spikes
- something that can tell you when it is failing
- something another engineer could run from your repo

That is the winning track.

---

## One-Line Plan

Build **one productionized AI gateway service** and use it to demonstrate Reliability Gold, Scalability Gold, strong Incident Response, and polished Documentation.
