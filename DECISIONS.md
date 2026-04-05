# Decisions

## Decision 1: Use Python + FastAPI

Reason:

- fast to build
- strong validation story with `Pydantic`
- easy testing setup
- good Prometheus and Docker ecosystem
- strong fit for backend-only hackathon work

## Decision 2: Start With Mocked Inference

Reason:

- avoids burning OpenAI credits
- avoids external provider instability early on
- makes tests deterministic
- makes caching easier to demonstrate
- keeps focus on production engineering, not model quality

Optional future mode:

- support a real provider later behind an environment variable

## Decision 3: No Public User-Created API Keys In Initial Scope

Reason:

- not required to win the hackathon
- adds complexity without helping the core quests enough
- introduces unnecessary abuse and credit-risk concerns

If auth is needed later, we can add a single internal demo API key.

## Decision 4: Optimize For Local Docker Compose Demo First

Reason:

- faster feedback loop
- lower setup risk
- easier to rehearse
- judges care more about proof than cloud complexity

## Decision 5: Backend-Only Submission

Reason:

- this hackathon rewards production engineering behavior
- frontend work is low-value for this judging rubric
- backend proof is faster and stronger

## Decision 6: Redis Is Mandatory

Reason:

- supports scalability gold story
- gives measurable performance improvement
- looks credible in architecture
- helps with the bottleneck narrative

## Decision 7: Nginx Is Mandatory

Reason:

- gives a clean load-balancing story
- helps the architecture feel production-shaped
- directly supports horizontal scaling proof

## Decision 8: Discord Webhook Is The Preferred Alert Sink

Reason:

- simpler than many alternatives
- visual and easy to demo
- enough for incident response proof

Setup can happen later in the project when alerting is implemented.

## Decision 9: Quest Prioritization

Priority order:

1. Reliability Gold
2. Scalability Gold
3. Documentation Silver+
4. Incident Response Silver or Gold

Reason:

- reliability and scalability give the strongest proof fastest
- incident response is valuable but more setup-heavy

## Decision 10: Keep The Product Surface Small

Allowed early endpoints:

- `GET /health`
- `POST /generate`
- `GET /metrics`

Reason:

- every extra endpoint increases implementation, test, and demo complexity
- a smaller system is easier to make look solid
