"""Redis cache layer for the gateway."""

import json
import logging
from typing import Optional

import redis

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[redis.Redis] = None


def get_client() -> Optional[redis.Redis]:
    global _client
    if _client is None:
        try:
            _client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=2,
            )
            _client.ping()
            logger.info("Redis connection established")
        except redis.ConnectionError:
            logger.warning("Redis unavailable; cache will be disabled")
            _client = None
    return _client


def cache_get(key: str) -> Optional[dict]:
    client = get_client()
    if client is None:
        return None
    try:
        raw = client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except (redis.RedisError, json.JSONDecodeError):
        return None


def cache_set(key: str, value: dict, ttl: int = 300) -> None:
    client = get_client()
    if client is None:
        return
    try:
        client.setex(key, ttl, json.dumps(value))
    except redis.RedisError:
        pass
