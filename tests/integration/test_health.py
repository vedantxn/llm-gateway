"""Integration tests for GET /health."""

import pytest


@pytest.mark.anyio
async def test_health_returns_200(client):
    response = await client.get("/health")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_health_response_body(client):
    response = await client.get("/health")
    body = response.json()
    assert body == {"status": "ok"}


@pytest.mark.anyio
async def test_health_content_type(client):
    response = await client.get("/health")
    assert response.headers["content-type"] == "application/json"
