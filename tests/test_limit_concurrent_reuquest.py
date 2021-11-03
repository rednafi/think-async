import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
from httpx import Response

import patterns.limit_concurrent_request as main


@pytest.mark.asyncio
@patch.object(main.httpx.AsyncClient, "get", return_value=Response(status_code=200))
@patch("patterns.limit_concurrent_request.asyncio.sleep", autospec=True)
async def test_make_request(mock_asyncio_sleep, mock_async_client_get):

    # Call 'make_request'.
    status_code = await main.make_request(url="dummy_url")

    # Assert.
    assert status_code == 200
    mock_asyncio_sleep.assert_awaited_once()
    mock_async_client_get.assert_awaited_once()


@pytest.mark.asyncio
@patch("patterns.limit_concurrent_request.make_request", autospec=True)
@patch("patterns.limit_concurrent_request.asyncio.sleep", autospec=True)
async def test_safe_make_request(mock_asyncio_sleep, mock_make_request, capsys):
    limit = asyncio.Semaphore(1)

    # Call 'safe_make_request'.
    for _ in range(5):
        await main.safe_make_request(url="dummy_url", limit=limit)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "limit reached" in out
    mock_asyncio_sleep.assert_awaited()
    mock_make_request.assert_awaited()


@pytest.mark.asyncio
@patch.object(main, "MAX_CONSUMERS", 1)
@patch("patterns.limit_concurrent_request.asyncio.gather", new_callable=AsyncMock)
@patch("patterns.limit_concurrent_request.safe_make_request", new_callable=Mock)
async def test_orchestrator(mock_safe_make_request, mock_asyncio_gather):

    # Call 'orchestrator'
    await main.orchestrator()

    # Assert.
    mock_safe_make_request.assert_called_once()
    mock_asyncio_gather.assert_awaited_once()
