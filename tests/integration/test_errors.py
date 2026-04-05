"""Integration tests for error handling and edge-case routes."""

import pytest


@pytest.mark.anyio
async def test_unknown_route_returns_404_json(client):
    response = await client.get("/nonexistent")

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "not_found"
    assert body["error"]["message"] == "resource not found"


@pytest.mark.anyio
async def test_404_content_type_is_json(client):
    response = await client.get("/does-not-exist")
    assert response.headers["content-type"] == "application/json"


# --- Metrics ---


@pytest.mark.anyio
async def test_metrics_returns_200(client):
    response = await client.get("/metrics")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_metrics_contains_expected_text(client):
    response = await client.get("/metrics")
    text = response.text

    assert "llm_gateway_up" in text
    assert 'service="llm-gateway"' in text
    assert "llm_gateway_process_memory_bytes" in text
    assert "llm_gateway_process_cpu_percent" in text


@pytest.mark.anyio
async def test_metrics_content_type(client):
    response = await client.get("/metrics")
    assert "text/plain" in response.headers["content-type"]


# --- Method not allowed ---


@pytest.mark.anyio
async def test_get_on_generate_returns_405(client):
    response = await client.get("/generate")
    assert response.status_code == 405
