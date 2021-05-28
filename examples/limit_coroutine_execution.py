from __future__ import annotations

import asyncio


async def echo(term: str, limit: asyncio.Semaphore) -> None:
    async with limit:
        print(term)
        await asyncio.sleep(0.1)
        if limit.locked():
            print(f"limit crossed, sleeping for {2} seconds")
            await asyncio.sleep(2)


async def main() -> None:
    limit = asyncio.Semaphore(3)  # type: asyncio.Semaphore
    consumers = [echo("Semaphore is awesome!", limit) for _ in range(9)]
    await asyncio.gather(*consumers)


asyncio.run(main())
