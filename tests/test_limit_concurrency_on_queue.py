import asyncio
from contextvars import ContextVar
from unittest.mock import patch

import patterns.limit_concurrency_on_queue as main


@patch("patterns.limit_concurrency_on_queue.asyncio.sleep", autospec=True)
async def test_foo(mock_asyncio_sleep, capsys):
    func_id = 42

    # Call 'foo'.
    await main.foo(func_id=func_id)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert f"Doing work - {func_id}" in out
    mock_asyncio_sleep.assert_awaited_once()


@patch("patterns.limit_concurrency_on_queue.asyncio.sleep", autospec=True)
async def test_producer(mock_asyncio_sleep, capsys):
    func_ids = (1, 2, 3)
    queue = asyncio.Queue(maxsize=3)

    # Call 'producer'.
    await main.producer(func_ids=func_ids, queue=queue)

    # Assert.
    out, err = capsys.readouterr()

    assert err == ""
    assert "Queue is full" in out
    assert queue.full() is True
    mock_asyncio_sleep.assert_awaited()


@patch("patterns.limit_concurrency_on_queue.foo", autospec=True)
@patch("patterns.limit_concurrency_on_queue.asyncio.sleep", autospec=True)
async def test_consumer(mock_foo, mock_asyncio_sleep, capsys):
    func_ids = (1, 2, 3)
    queue = asyncio.Queue(maxsize=3)

    # Call 'producer'.
    await main.producer(func_ids=func_ids, queue=queue)

    # Call 'consumer'.
    await main.consumer(queue=queue)

    # Assert.
    out, err = capsys.readouterr()

    assert "Queue is full" in out
    assert err == ""
    assert queue.empty() is True
    mock_asyncio_sleep.assert_awaited()
    mock_foo.assert_awaited()


@patch.object(main, "CONCURRENT_TASK_COUNT", ContextVar("test_limit", default=50))
@patch("patterns.limit_concurrency_on_queue.asyncio.sleep", autospec=True)
async def test_orchestrator(mock_asyncio_sleep, capsys):

    # Call the orchestrator.
    await main.orchestrator()

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Doing work" in out
    mock_asyncio_sleep.assert_awaited()
