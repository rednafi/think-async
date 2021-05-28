"""
This script makes 30 GET requests to a URL. However, it sends them in a batch of
10 requests and sleeps for 2 seconds between subsequent requests. The effective
concurrency is roughly 3 requests per second.

To run the script, install httpx with `pip install httpx`. Then run-

`time python -m examples.limit_concurrent_request`


"""

from __future__ import annotations

import asyncio

import httpx

MAX_CONSUMERS = 30


async def make_request(url: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print(response.status_code)
        await asyncio.sleep(1)
        return response.status_code


async def safe_make_request(url: str, limit: asyncio.Semaphore) -> int:
    async with limit:
        result = await make_request(url)

        if limit.locked():
            print("\nlimit reached, sleeping for 2 seconds...\n")
            await asyncio.sleep(1.5)

        return result


async def main() -> None:
    token = "c1u0d7qad3ifani3q2rg"
    url = f"https://finnhub.io/api/v1/forex/rates?base=USD&token={token}"
    limit = asyncio.Semaphore(10)      # type: asyncio.Semaphore

    tasks = [safe_make_request(url, limit) for _ in range(MAX_CONSUMERS)]
    await asyncio.gather(*tasks)


asyncio.run(main())
