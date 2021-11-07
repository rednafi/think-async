from __future__ import annotations

import asyncio
import hashlib

import aioredis
from aioredis.client import Redis


class TooManyRequests(Exception):
    pass


def redis_pool() -> Redis:
    connection_pool = aioredis.ConnectionPool(max_connections=100)
    REDIS_POOL = aioredis.Redis(
        host="127.0.0.1", port=6379, db=0, connection_pool=connection_pool
    )
    return REDIS_POOL


REDIS_POOL = redis_pool()


class RateLimit:
    def __init__(
        self,
        header: dict[str, str],
        prefix: str | None = None,
        rps: int = 100,  # 10 requests per second.
        redis_pool: Redis = REDIS_POOL,
    ) -> None:
        self._header = header
        self._prefix = prefix
        self._rps = rps
        self._redis_pool = redis_pool
        self._ttl = 10  # Time to live = 10 seconds.

    async def _limiter(self, target_attr: str) -> None:
        hash_val = hashlib.sha1(
            bytes(target_attr, encoding="raw_unicode_escape"), usedforsecurity=False
        ).hexdigest()

        if self._prefix:
            key = f"rate_limit:{self._prefix}:{hash_val}"
        else:
            key = f"rate_limit:{hash_val}"

        value = await self._redis_pool.get(key)

        if value is None:
            await self._redis_pool.setex(key, self._ttl, self._rps * self._ttl)
        else:
            if int(value) > 0:
                await self._redis_pool.decrby(key, 1)
            else:
                raise TooManyRequests("429")

    async def rate_limit(self) -> None:
        if auth_token := self._header.get("Authorization"):
            await self._limiter(auth_token)

        elif host_ip := self._header.get("Host"):
            await self._limiter(host_ip)


async def func_to_be_rate_limited(call_count: int) -> None:
    header = {"Authorization": "helloworld"}
    rl = RateLimit(header, rps=5)
    await rl.rate_limit()
    print(f'Func call {call_count}')


async def orchestrator() -> None:
    for call_count in range(100):
        await func_to_be_rate_limited(call_count=call_count)


if __name__ == "__main__":
    asyncio.run(orchestrator())
