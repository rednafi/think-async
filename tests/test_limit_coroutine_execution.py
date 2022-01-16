import asyncio
from unittest.mock import patch

import patterns.limit_coroutine_execution as main


@patch("patterns.limit_coroutine_execution.asyncio.sleep", autospec=True)
async def test_echo(mock_asyncio_sleep, capsys):
    limit = asyncio.Semaphore(1)

    # Call 'echo'.
    for _ in range(3):
        await main.echo(term="testing echo", limit=limit)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "limit crossed" in out
    mock_asyncio_sleep.assert_awaited()


@patch(
    "patterns.limit_coroutine_execution.asyncio.Semaphore",
    autospec=True,
    return_value=asyncio.Semaphore(1),
)
@patch("patterns.limit_coroutine_execution.asyncio.sleep", autospec=True)
async def test_orchestrator(mock_asyncio_sleep, mock_asyncio_semaphore, capsys):

    # Call 'orchestrator'.
    await main.orchestrator()

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Semaphore is awesome" in out
    assert "limit crossed" in out
    mock_asyncio_sleep.assert_awaited()
    mock_asyncio_semaphore.assert_called_once()
