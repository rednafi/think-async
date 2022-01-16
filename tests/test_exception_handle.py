import asyncio
from unittest.mock import patch

import pytest

import patterns.exception_handle as main


async def test_func(capsys):

    # Call 'func' with mocked 'asyncio.sleep'.
    with pytest.raises(ZeroDivisionError):
        await main.func(0)

    out, err = capsys.readouterr()

    # Assert
    assert err == ""
    assert "doing work" in out
    assert "work done" not in out


@patch("patterns.exception_handle.asyncio.sleep", autospec=True)
async def test_producer(mock_asyncio_sleep):
    queue = asyncio.Queue()

    # Call 'producer'.
    await main.producer(q_args=queue)

    # Assert.
    mock_asyncio_sleep.assert_awaited_once()
    assert queue.qsize() == 5


@patch("patterns.exception_handle.asyncio.sleep", autospec=True)
@patch("patterns.exception_handle.func", autospec=True)
async def test_consumer(mock_asyncio_sleep, mock_func, capsys):
    queue = asyncio.Queue()

    # Call 'producer'.
    await main.producer(q_args=queue)

    # Call 'consumer'.
    await main.consumer(q_args=queue)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "sleeping for" in out

    assert queue.qsize() == 0
    mock_asyncio_sleep.assert_awaited()
    mock_func.assert_awaited()


@patch(
    "patterns.exception_handle.asyncio.Queue",
    autospec=True,
    return_value=asyncio.Queue(),
)
@patch("patterns.exception_handle.asyncio.sleep", autospec=True)
async def test_orchestrator(mock_asyncio_sleep, mock_asyncio_queue, capsys):
    # Call 'orchestrator'.

    with pytest.raises(ZeroDivisionError):
        await main.orchestrator()

    out, err = capsys.readouterr()

    # Assert
    assert err == ""
    assert "doing work" in out
    assert "work done" not in out

    mock_asyncio_sleep.assert_awaited()
    mock_asyncio_queue.assert_called()
