from __future__ import annotations

import asyncio
import enum
from types import TracebackType
from typing import Any, Optional, Type


def ephemera(
    timeout: Optional[float] = None,
    timeout_at: Optional[float] = None,
) -> Timeout:
    if all((timeout, timeout_at)):
        raise TypeError("passing both 'timeout' and 'timeout_at' is not allowed")

    loop = asyncio.get_running_loop()
    if timeout:
        # Here, loop.time is basically time.monotonic.
        deadline = loop.time() + timeout
    else:
        deadline = timeout_at  # type: ignore

    return Timeout(deadline)


class _State(str, enum.Enum):
    INIT = "INIT"
    ENTER = "ENTER"
    TIMEOUT = "TIMEOUT"
    EXIT = "EXIT"


class Timeout:
    def __init__(self, deadline: float) -> None:
        self._loop = asyncio.get_running_loop()
        self._task = asyncio.current_task()
        self._state = _State.INIT
        self._timeout_handler = None  # type: Optional[asyncio.TimerHandle]
        self.countdown(deadline)

    async def __aenter__(self) -> Timeout:
        if self._state != _State.INIT:
            raise RuntimeError(f"invalid state {self._state}")

        self._state = _State.ENTER
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        if exc_type is asyncio.CancelledError and self._state == _State.TIMEOUT:
            self._timeout_handler = None
            raise asyncio.TimeoutError

        # timeout didn't work and didn't raise TimeoutError.
        self._state = _State.EXIT
        self.calloff()

    def calloff(self) -> None:
        if self._state not in (_State.INIT, _State.ENTER):
            raise RuntimeError(f"invalid state {self._state}")

        if self._timeout_handler:
            self._timeout_handler.cancel()
            self._timeout_handler = None

    def countdown(self, deadline: float) -> None:
        """Advance timeout on the abdelay seconds.
        If new deadline is in the past
        the timeout is raised immediatelly.
        """
        if self._state == _State.EXIT:
            raise RuntimeError("cannot reschedule after exit from context manager")
        if self._state == _State.TIMEOUT:
            raise RuntimeError("cannot reschedule expired timeout")
        if self._timeout_handler is not None:
            self._timeout_handler.cancel()

        now = self._loop.time()
        if now >= deadline:
            self._timeout_handler = None
            if self._state == _State.INIT:
                raise asyncio.TimeoutError
            else:
                # state is ENTER
                raise asyncio.CancelledError

        self._timeout_handler = self._loop.call_at(
            deadline, self._on_timeout, self._task
        )

    def _on_timeout(self, task: asyncio.Task) -> None:
        task.cancel()
        self._state = _State.TIMEOUT


## Usage
async def func(delay: float) -> None:
    print(f"doing work for {delay} sec")
    await asyncio.sleep(delay)

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
    q_args = asyncio.Queue()  # type: asyncio.Queue

    producers = [asyncio.create_task(producer(q_args))]
    consumers = [asyncio.create_task(consumer(q_args)) for _ in range(5)]

    producers.extend(consumers)

    async with ephemera(timeout=2):
        done, pending = await asyncio.wait(producers)
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
