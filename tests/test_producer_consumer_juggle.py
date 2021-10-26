import asyncio
from unittest.mock import AsyncMock, patch

import pytest

import patterns.producer_consumer_juggle as main


@pytest.mark.asyncio
@patch("patterns.producer_consumer_juggle.itertools.cycle", autospec=True)
@patch("patterns.producer_consumer_juggle.asyncio.sleep", autospec=True)
async def test_producer(mock_async_sleep, mock_itertools_cycle, capsys):
    # Mock function calls.
    mock_async_sleep.return_value = None
    mock_itertools_cycle.return_value = [1, 2, 3]

    # Call the producer function.
    queue = asyncio.Queue()
    event = asyncio.Event()

    await main.producer(queue=queue, event=event)

    # Assert console output.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Running producer" in out

    # Assert queue size.
    assert queue.qsize() == 3

    # Assert event mutation.
    assert event.is_set() is True


@pytest.mark.asyncio
@patch("patterns.producer_consumer_juggle.itertools.cycle", autospec=True)
@patch("patterns.producer_consumer_juggle.asyncio.sleep", autospec=True)
async def test_consumer(mock_async_sleep, mock_itertools_cycle, capsys):

    # Mock function calls.
    mock_async_sleep.return_value = None
    mock_itertools_cycle.return_value = [1, 2, 3]

    # Call the producer function.
    queue = asyncio.Queue()
    event = asyncio.Event()

    # Call the producer to fill in the queue.
    await main.producer(queue=queue, event=event)

    # Call the consumer to consume the tasks.
    await main.consumer(queue=queue, event=event, stop_after=3)

    # Assert output.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Running consumer" in out

    # Assert queue size.
    assert queue.qsize() == 0

    # Assert event mutation.
    assert event.is_set() is True


@pytest.mark.asyncio
@patch("patterns.producer_consumer_juggle.asyncio.gather")
@patch("patterns.producer_consumer_juggle.asyncio.create_task", autospec=True)
@patch("patterns.producer_consumer_juggle.asyncio.Event", autospec=True)
@patch("patterns.producer_consumer_juggle.asyncio.Queue", autospec=True)
@patch("patterns.producer_consumer_juggle.consumer", autospec=True)
@patch("patterns.producer_consumer_juggle.producer", autospec=True)
async def test_main(
    mock_producer,
    mock_consumer,
    mock_asyncio_queue,
    mock_asyncio_event,
    mock_asyncio_create_task,
    mock_asyncio_gather,
):
    async_mock = AsyncMock()
    mock_asyncio_gather.return_value = async_mock()

    # Call the orchestrator.
    await main.main()

    mock_asyncio_event.assert_called_once()
    mock_asyncio_queue.assert_called_once()
    mock_consumer.assert_called()
    mock_producer.assert_called_once()
    mock_asyncio_create_task.assert_called()
    mock_asyncio_gather.assert_called_once()
