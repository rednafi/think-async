import importlib
import logging
import pickle
import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fakeredis.aioredis import FakeRedis

import patterns.async_redis_queue as main


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def test_log_level(caplog):

    # Assert.
    with caplog.at_level(logging.INFO):
        main.logger.info("enqueue")
        assert "enqueue" in caplog.text

    assert main.logger.name == main.__name__
    assert main.logger.parent.name == "root"


@patch("patterns.async_redis_queue.uvloop.install", autospec=True)
def test_uvloop_install_call(mock_uvloop_install):

    # Import the 'async_redis_queue' module again.
    importlib.reload(main)
    mock_uvloop_install.assert_called_once()


async def test_simple_task(capsys):

    # Make a mock version of async function `main.foo`.
    mock_func = AsyncMock()
    mock_func.side_effect = lambda num: print(num)

    # Call 'SimpleTask'.
    num = 42
    st = main.SimpleTask(mock_func, num=num)

    # Call 'SimpleTask.process_task'.
    await st.process_task()

    # Assert.
    assert st.func == mock_func
    assert st.args == tuple()
    assert st.kwargs["num"] == num
    out, err = capsys.readouterr()
    assert err == ""
    assert "42" in out


class TestRedisQueue:
    @patch(
        "patterns.async_redis_queue.aioredis.from_url",
        new_callable=lambda: FakeRedis.from_url,
    )
    def setup(self, mock_aioredis_from_url, *args):
        # Mock instances.
        self.mock_aioredis_from_url = mock_aioredis_from_url

        # Call 'Queue'.
        self.redis_queue = main.RedisQueue(
            broker=main.aioredis.from_url("redis://localhost:6379/0"),
            result_backend=main.aioredis.from_url("redis://localhost:6379/1"),
            queue_name="test_queue",
        )

    def test_init(self):
        # Assert attributes.
        assert isinstance(self.redis_queue.broker, FakeRedis) is True
        assert isinstance(self.redis_queue.result_backend, FakeRedis) is True
        assert self.redis_queue.queue_name == "test_queue"

    async def test_enqueue_invoke_pickle_error(self, caplog):
        # Queue.enqueue should raise pickle error if 'func' object aren't the same.
        with caplog.at_level(logging.INFO):
            with pytest.raises(pickle.PickleError):
                await self.redis_queue.enqueue(func=AsyncMock(), start=1, end=2)


    async def test_enqueue(self, caplog):
        with caplog.at_level(logging.INFO):
            # Call 'enqueue' with the real 'foo' function.
            task_id = await self.redis_queue.enqueue(func=main.foo, start=1, end=2)

        # Assert.
        assert is_valid_uuid(task_id) is True

    async def test_dequeue(self, caplog):
        # Call 'enqueue'.
        await self.redis_queue.enqueue(func=main.foo, start=1, end=2)

        # Call 'dequeue'.
        with caplog.at_level(logging.INFO):
            await self.redis_queue.dequeue()

        assert "Kwargs: {'start': 1, 'end': 2}" in caplog.text
        assert "Task processing complete" in caplog.text

    async def test_get_length(self):
        # Call 'enqueue'.
        await self.redis_queue.enqueue(func=main.foo, start=1, end=2)

        # Call 'get_length'.
        redis_queue_length = await self.redis_queue.get_length()

        # Assert.
        assert redis_queue_length == 1


@patch("patterns.async_redis_queue.RedisQueue", autospec=True)
async def test_worker(mock_redis_queue):
    # Mock 'setup'.
    mock_redis_queue = main.RedisQueue(
        broker=main.aioredis.from_url("redis://localhost:6379/0"),
        result_backend=main.aioredis.from_url("redis://localhost:6379/1"),
        queue_name="test_queue",
    )

    mock_redis_queue.get_length.return_value = 42

    # Call 'worker'.
    await main.worker(queue=mock_redis_queue)

    # Assert.
    mock_redis_queue.dequeue.assert_awaited_with()
    mock_redis_queue.get_length.assert_awaited_with()


@patch("patterns.async_redis_queue.random.randint", autospec=True, return_value=42)
@patch("patterns.async_redis_queue.asyncio.sleep", autospec=True)
async def test_foo(mock_asyncio_sleep, mock_random_randint):
    # Call 'foo'.
    result = await main.foo(start=1, end=20)

    # Assert.
    assert result == 42
    mock_asyncio_sleep.assert_awaited_once()
    mock_random_randint.assert_called_once_with(1, 20)


@patch("patterns.async_redis_queue.random.randint", autospec=True, return_value=42)
@patch("patterns.async_redis_queue.asyncio.sleep", autospec=True)
@patch(
    "patterns.async_redis_queue.aioredis.from_url",
    autospec=True,
    return_value=FakeRedis.from_url("redis://localhost:6379/0"),
)
async def test_orchestrator(
    mock_aioredis_from_url, mock_asyncio_sleep, mock_random_randint, caplog
):
    # Call 'orchestrator'.
    with caplog.at_level(logging.INFO):
        await main.orchestrator()

    # Assert.
    mock_asyncio_sleep.assert_awaited()
    mock_random_randint.assert_called()
    mock_aioredis_from_url.assert_called()
    assert mock_asyncio_sleep.call_count == 10
    assert mock_random_randint.call_count == 10
    assert mock_aioredis_from_url.call_count == 2
