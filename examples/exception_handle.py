import asyncio


async def func(delay: float) -> None:
    print(f"doing work for {delay} sec")
    await asyncio.sleep(delay)
    1 // 0

    print("work done")


async def producer(q_args: asyncio.Queue) -> None:
    for i in range(0, 5):
        await q_args.put(i)

    await asyncio.sleep(0)


async def consumer(q_args: asyncio.Queue) -> None:
    while q_args.qsize():
        delay = await q_args.get()
        await func(delay)
        print("sleeping for 1 sec")
        await asyncio.sleep(1)
        q_args.task_done()


async def orchestrator() -> None:
    q_args = asyncio.Queue()  # type: asyncio.Queue[int]

    producers = [asyncio.create_task(producer(q_args))]
    consumers = [asyncio.create_task(consumer(q_args)) for _ in range(5)]

    producers.extend(consumers)

    done, pending = await asyncio.wait(
        producers,
        return_when=asyncio.FIRST_EXCEPTION,
    )
    for fut in done:
        try:
            if exc := fut.exception():
                raise exc
        except asyncio.exceptions.InvalidStateError:
            pass

    for t in pending:
        t.cancel()

    await q_args.join()


async def main() -> None:
    await orchestrator()


asyncio.run(main())
