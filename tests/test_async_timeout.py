import asyncio
import time
from enum import Enum
from unittest.mock import patch

import pytest

import patterns.async_timeout as main


def test_state():
    # Call '_State'.
    assert issubclass(main._State, Enum)
    assert list(main._State) == ["INIT", "ENTER", "TIMEOUT", "EXIT"]

    for attr in main._State:
        # Check enum integrity.
        assert isinstance(attr, Enum)

        # Check repr integrity, e.g `<_State.INIT: 'INIT'>`.
        assert attr.__repr__() == f"<{main._State.__name__}.{attr.name}: '{attr.name}'>"


async def test_ephemera_with_invalid_args():
    timeout = 0.1

    # Passing both 'timeout' and 'timeout_at' should raise a type error.
    with pytest.raises(TypeError):
        async with main.ephemera(timeout=timeout, timeout_at=2.0):
            await asyncio.sleep(timeout + 0.1)


async def test_ephemera_with_timeout():
    timeout = 0.1
    with pytest.raises(asyncio.TimeoutError):
        async with main.ephemera(timeout=timeout):
            await asyncio.sleep(timeout + 0.1)


async def test_ephemera_with_timeout_at():

    timeout_at = time.monotonic() + 0.1
    with pytest.raises(asyncio.TimeoutError):
        async with main.ephemera(timeout_at=timeout_at):
            await asyncio.sleep(1)


@patch("patterns.async_timeout.asyncio.sleep", autospec=True)
async def test_func(mock_asyncio_sleep, capsys):
    delay = 1

    # Call 'func'.
    await main.func(delay=delay)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert f"doing work for {delay} sec" in out
    assert "work done" in out
    mock_asyncio_sleep.assert_awaited_once_with(delay)


@patch("patterns.async_timeout.asyncio.sleep", autospec=True)
async def test_producer(mock_async_sleep):

    # Call 'producer'.
    queue = asyncio.Queue()

    await main.producer(q_args=queue)

    # Assert.
    assert queue.qsize() == 5
    mock_async_sleep.assert_awaited_with(0)


@patch("patterns.async_timeout.asyncio.sleep", autospec=True)
async def test_consumer(mock_async_sleep, capsys):

    # Call 'producer'.
    queue = asyncio.Queue()
    await main.producer(q_args=queue)

    # Call 'consumer'.
    await main.consumer(q_args=queue)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "doing work for 0 sec" in out
    assert "doing work for 4 sec" in out
    assert "sleeping for 1 sec" in out
    assert queue.qsize() == 0
    mock_async_sleep.assert_awaited()


@patch("patterns.async_timeout.ephemera", autospec=True)
@patch(
    "patterns.async_timeout.asyncio.wait",
    autospec=True,
)
@patch("patterns.async_timeout.asyncio.create_task", autospec=True)
@patch("patterns.async_timeout.asyncio.Queue", autospec=True)
@patch("patterns.async_timeout.consumer", autospec=True)
@patch("patterns.async_timeout.producer", autospec=True)
async def test_orchestrator(
    mock_producer,
    mock_consumer,
    mock_asyncio_queue,
    mock_asyncio_create_task,
    mock_asyncio_wait,
    mock_ephemera,
):
    # Mocking 'asyncio.wait'.
    done_fut, pending_fut = asyncio.Future(), asyncio.Future()
    done_fut.set_result(42)
    mock_asyncio_wait.return_value = [done_fut], [pending_fut]

    # Call the orchestrator.
    await main.orchestrator()

    mock_asyncio_queue.assert_called_once()
    mock_consumer.assert_called()
    mock_producer.assert_called_once()
    mock_asyncio_create_task.assert_called()
    mock_asyncio_wait.assert_called_once()
    mock_ephemera.assert_called_once()
    mock_asyncio_queue().join.assert_awaited_once()
