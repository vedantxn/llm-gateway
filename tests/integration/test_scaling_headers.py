"""Integration tests for cache and routing headers."""

import pytest


@pytest.mark.anyio
async def test_generate_sets_cache_miss_header_on_uncached_request(client):
    response = await client.post("/generate", json={"prompt": "hello headers"})

    assert response.status_code == 200
    assert response.headers["x-cache"] == "MISS"
    assert response.headers["x-served-by"]


@pytest.mark.anyio
async def test_generate_sets_cache_hit_header_when_cached_response_exists(client, monkeypatch):
    from app.api import routes

    monkeypatch.setattr(
        routes,
        "cache_get",
        lambda _: {"output": "cached output"},
    )
    monkeypatch.setattr(routes, "generate_output", lambda _: (_ for _ in ()).throw(AssertionError("cache miss path should not run")))

    response = await client.post("/generate", json={"prompt": "hello headers"})

    assert response.status_code == 200
    assert response.headers["x-cache"] == "HIT"
    assert response.headers["x-served-by"]
    assert response.headers["x-request-id"].startswith("req_")
    assert response.json()["id"] == response.headers["x-request-id"]
    assert response.json()["output"] == "cached output"
    assert response.json()["cached"] is True
