from __future__ import annotations

import json
import os
from typing import Any


class RedisJsonCache:
    def __init__(self, redis_url: str | None = None, ttl_seconds: int = 60) -> None:
        self._redis_url = redis_url or os.getenv("REDIS_URL", "redis://redis:6379/0")
        self._ttl_seconds = ttl_seconds
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client

        try:
            import redis
        except Exception:
            return None

        try:
            self._client = redis.Redis.from_url(
                self._redis_url,
                decode_responses=True,
            )
        except Exception:
            self._client = None

        return self._client

    def get_json(self, key: str) -> Any | None:
        client = self._get_client()
        if client is None:
            return None

        try:
            cached_value = client.get(key)
        except Exception:
            return None

        if cached_value is None:
            return None

        try:
            return json.loads(cached_value)
        except json.JSONDecodeError:
            return None

    def set_json(self, key: str, value: Any) -> None:
        client = self._get_client()
        if client is None:
            return

        try:
            payload = json.dumps(value)
            client.setex(key, self._ttl_seconds, payload)
        except Exception:
            return
