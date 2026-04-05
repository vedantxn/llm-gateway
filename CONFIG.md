# Configuration

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `OPENAI_API_KEY` | No | unset | Optional future real-model mode |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis connection string |
| `MOCK_PROCESSING_DELAY_MS` | No | `50` | Simulated upstream processing latency on cache miss |
| `DISCORD_WEBHOOK_URL` | Yes for alerts | unset | Discord webhook used by the alert relay |
| `ENVIRONMENT` | No | `development` | Environment label for the app |

## Notes

- `DISCORD_WEBHOOK_URL` must be present in `.env` for live Discord notifications.
- If the alert relay returns `502 Bad Gateway`, the most likely cause is an invalid or revoked Discord webhook. Create a fresh webhook in Discord and replace the value in `.env`.
- `.env` is ignored by git and should never be committed.
- For hackathon demo reliability, mocked inference remains the default path.
