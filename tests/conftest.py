"""Shared fixtures for tests."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import create_app


@pytest.fixture()
def app():
    """Create a fresh application instance for each test."""
    return create_app()


@pytest.fixture()
async def client(app):
    """Async HTTP client backed by the ASGI app — no running server needed."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
