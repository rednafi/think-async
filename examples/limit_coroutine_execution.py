from __future__ import annotations
import asyncio


async def echo(term: str, limit: asyncio.Semaphore):
    async with limit:
        print(term)
        await asyncio.sleep(0)
        if limit.locked():
            print(f"\nlimit crossed, sleeping for {2} seconds\n")
        await asyncio.sleep(2)


async def main():
    limit = asyncio.Semaphore(3)
    consumers = [echo("Semaphore is awesome!", limit) for _ in range(9)]
    await asyncio.gather(*consumers)


asyncio.run(main())
