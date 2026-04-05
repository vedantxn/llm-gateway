# Reliability & Error Handling

This document describes how the llm-gateway API handles errors and what clients can expect in failure scenarios.

## Error Response Structure

Every error response follows a consistent JSON shape:

```json
{
  "error": {
    "code": "<error_code>",
    "message": "<human-readable description>"
  }
}
```

The `code` field is machine-readable. The `message` field is safe to display to end users.

## Error Codes

| Code | HTTP Status | When It Occurs |
|------|-------------|----------------|
| `invalid_request` | `422` | Request body fails validation (missing fields, wrong types, constraint violations) |
| `not_found` | `404` | The requested route does not exist |
| `internal_error` | `500` | An unexpected server error occurred |

## Validation Behavior

The `POST /generate` endpoint validates the request body before processing:

| Condition | Result |
|-----------|--------|
| `prompt` field is missing | `422` — `"prompt is required"` |
| `prompt` is an empty string | `422` — `"prompt must not be empty"` |
| `prompt` is whitespace only | `422` — `"prompt must not be empty"` (trimmed to empty) |
| `prompt` is not a string | `422` — `"prompt must be a string"` |
| `prompt` exceeds 1000 characters | `422` — `"prompt must be at most 1000 characters"` |
| `prompt` has leading/trailing whitespace | Accepted — whitespace is trimmed silently |

Validation is performed by the Pydantic schema layer. The API never returns raw Pydantic or FastAPI error details to clients.

## 404 Behavior

Any request to a route that does not exist receives:

```json
{
  "error": {
    "code": "not_found",
    "message": "resource not found"
  }
}
```

The response is always JSON, never the default HTML 404.

## 500 Behavior

If an unhandled exception occurs inside a route handler, the API returns:

```json
{
  "error": {
    "code": "internal_error",
    "message": "internal server error"
  }
}
```

Internal details (stack traces, variable values) are **never** exposed to the client.

## What Clients Will See

- **Success responses** follow the documented response schemas (JSON with typed fields).
- **Error responses** always use the `{"error": {"code", "message"}}` structure.
- **Content-Type** is always `application/json` for success and error responses, except for `GET /metrics` which returns `text/plain`.
- **No HTML** is ever returned for any endpoint.

## What Clients Will Not See

- Raw exception messages or stack traces
- Framework-generated error detail arrays
- Database or infrastructure internals
- Debug information of any kind

## Testing

All error behavior is covered by automated tests in `tests/integration/test_errors.py` and `tests/integration/test_generate.py`. Tests verify both the HTTP status code and the exact error response structure.
