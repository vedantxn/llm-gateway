"""Integration tests for POST /generate."""

import pytest


# --- Success cases ---


@pytest.mark.anyio
async def test_generate_success(client):
    response = await client.post("/generate", json={"prompt": "hello world"})

    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "output" in body
    assert "cached" in body
    assert isinstance(body["cached"], bool)


@pytest.mark.anyio
async def test_generate_id_format(client):
    response = await client.post("/generate", json={"prompt": "test"})
    body = response.json()

    # request id must be req_ followed by 8 hex chars
    assert body["id"].startswith("req_")
    assert len(body["id"]) == 12


@pytest.mark.anyio
async def test_generate_output_contains_prompt(client):
    response = await client.post("/generate", json={"prompt": "greetings"})
    body = response.json()

    assert "greetings" in body["output"]


@pytest.mark.anyio
async def test_generate_trims_whitespace(client):
    response = await client.post("/generate", json={"prompt": "  padded prompt  "})
    body = response.json()

    # The trimmed prompt should be reflected in the output
    assert "padded prompt" in body["output"]
    assert "  padded prompt  " not in body["output"]


# --- Validation failures ---


@pytest.mark.anyio
async def test_generate_missing_prompt(client):
    response = await client.post("/generate", json={})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "invalid_request"
    assert "prompt" in body["error"]["message"].lower()


@pytest.mark.anyio
async def test_generate_empty_prompt(client):
    response = await client.post("/generate", json={"prompt": ""})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "invalid_request"
    assert "empty" in body["error"]["message"].lower()


@pytest.mark.anyio
async def test_generate_whitespace_only_prompt(client):
    response = await client.post("/generate", json={"prompt": "   "})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "invalid_request"
    assert "empty" in body["error"]["message"].lower()


@pytest.mark.anyio
async def test_generate_wrong_prompt_type(client):
    response = await client.post("/generate", json={"prompt": 12345})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "invalid_request"
    assert "string" in body["error"]["message"].lower()


@pytest.mark.anyio
async def test_generate_oversized_prompt(client):
    long_prompt = "x" * 1001
    response = await client.post("/generate", json={"prompt": long_prompt})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "invalid_request"
    assert "1000" in body["error"]["message"]
