import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest

import patterns.inequal_producer_consumer as main


@pytest.mark.asyncio
@patch(
    "patterns.inequal_producer_consumer.itertools.cycle",
    autospec=True,
    return_value=[1, 2, 3, 0, 1],
)
@patch("patterns.inequal_producer_consumer.asyncio.sleep", autospec=True)
async def test_generate_number(mock_asyncio_sleep, mock_itertools_cycle):
    # Call 'generate_number' function.

    results = []
    async for i in main.generate_number():
        results.append(i)

    # Assert.
    assert results == [1, 2, 3, 0, 1]
    mock_itertools_cycle.assert_called_once()
    mock_asyncio_sleep.assert_awaited()


@pytest.mark.asyncio
@patch(
    "patterns.inequal_producer_consumer.itertools.cycle",
    autospec=True,
    return_value=[1, 2, 3, 0, 1],
)
@patch("patterns.inequal_producer_consumer.asyncio.sleep", autospec=True)
async def test_producer(mock_asyncio_sleep, mock_itertools_cycle):
    queue = asyncio.Queue()
    event = asyncio.Event()

    await main.producer(result_queue=queue, event=event)

    assert queue.qsize() == 4
    assert event.is_set() is True
    mock_itertools_cycle.assert_called_once()
    mock_asyncio_sleep.assert_awaited()


@pytest.mark.asyncio
@patch.object(main, "MAX_CONSUMERS", 1)
@patch(
    "patterns.inequal_producer_consumer.itertools.cycle",
    autospec=True,
    return_value=[1, 2, 3, 0, 1],
)
@patch("patterns.inequal_producer_consumer.asyncio.sleep", autospec=True)
async def test_consumer(*args):
    queue = asyncio.Queue()
    event = asyncio.Event()
    limit = asyncio.Semaphore(1)

    # Call the 'producer' to fill the queue.
    await main.producer(result_queue=queue, event=event)

    # Call the 'consumer' to empty the queue.
    with pytest.raises(SystemExit):
        await main.consumer(result_queue=queue, event=event, limit=limit, stop_after=4)

    assert queue.qsize() == 0


@pytest.mark.asyncio
@patch.object(main, "MAX_CONSUMERS", 1)
@patch(
    "patterns.inequal_producer_consumer.asyncio.gather",
    autospec=True,
    side_effect=AsyncMock(),
)
@patch("patterns.inequal_producer_consumer.asyncio.create_task", autospec=True)
@patch("patterns.inequal_producer_consumer.asyncio.Event", autospec=True)
@patch("patterns.inequal_producer_consumer.asyncio.Queue", autospec=True)
@patch("patterns.inequal_producer_consumer.consumer", autospec=True)
@patch("patterns.inequal_producer_consumer.producer", new_callable=Mock())
async def test_orchestrator(
    mock_producer,
    mock_consumer,
    mock_asyncio_queue,
    mock_asyncio_event,
    mock_asyncio_create_task,
    mock_asyncio_gather,
):

    # Call the 'main' function.
    await main.orchestrator()

    mock_asyncio_event.assert_called_once()
    mock_asyncio_queue.assert_called_once()
    mock_consumer.assert_called()
    mock_producer.assert_called_once()
    mock_asyncio_create_task.assert_called()
    mock_asyncio_gather.assert_called_once()
    assert main.MAX_CONSUMERS == 1
    mock_asyncio_queue().join.assert_awaited_once()
