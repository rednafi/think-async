from unittest.mock import patch

import fakeredis.aioredis  # aioredis 2.0 fake.
import pytest

import patterns.async_redis_rate_limit as main


def test_too_many_requests():
    # Call 'TooManyRequests'.

    with pytest.raises(main.TooManyRequests):
        raise main.TooManyRequests("429: Too many requests.")


@pytest.mark.asyncio
async def test_rate_limit():

    # Call 'RateLimit'.
    rl = main.RateLimit(
        rps=1,
        header={"Authorization": "dummy_auth"},
        redis_pool=fakeredis.aioredis.FakeRedis(),
    )

    with pytest.raises(main.TooManyRequests):
        for _ in range(20):
            await rl.rate_limit()


@pytest.mark.asyncio
@patch(
    "patterns.async_redis_rate_limit.RateLimit",
    autospec=True,
    return_value=main.RateLimit(
        rps=1,
        header={"Authorization": "dummy_auth"},
        redis_pool=fakeredis.aioredis.FakeRedis(),
    ),
)
async def test_func_to_be_rate_limited(mock_rate_limit, capsys):

    # Call 'func_to_be_rate_limited'.
    with pytest.raises(main.TooManyRequests):
        for i in range(20):
            await main.func_to_be_rate_limited(call_count=i)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Func call 1" and "Func call 10" in out
    mock_rate_limit.assert_called()


@pytest.mark.asyncio
@patch(
    "patterns.async_redis_rate_limit.RateLimit",
    autospec=True,
    return_value=main.RateLimit(
        rps=1,
        header={"Authorization": "dummy_auth"},
        redis_pool=fakeredis.aioredis.FakeRedis(),
    ),
)
async def test_orchestrator(mock_rate_limit, capsys):

    # Call 'func_to_be_rate_limited'.
    with pytest.raises(main.TooManyRequests):
        await main.orchestrator()

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Func call 1" and "Func call 10" in out
    mock_rate_limit.assert_called()
