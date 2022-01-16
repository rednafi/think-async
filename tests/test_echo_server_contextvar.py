from unittest.mock import Mock, patch

import patterns.echo_server_contextvar as main


@patch.object(main, "client_addr_var", Mock())
def test_render_goodbye(capsys):

    # Call 'render_goodbye'
    goodbye_string = main.render_goodbye()
    print(goodbye_string)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Good bye, client @" in out


@patch("patterns.echo_server_contextvar.asyncio.start_server", autospec=True)
@patch("patterns.echo_server_contextvar.asyncio.sleep", autospec=True)
async def test_server(mock_asyncio_sleep, mock_asyncio_start_server):
    stop_after = 5

    # Call 'server()'.
    await main.server(stop_after=stop_after)

    # Assert.
    assert mock_asyncio_sleep.call_count == stop_after

    args = main.handle_request, "127.0.0.1", 8081
    mock_asyncio_start_server.assert_called_once_with(*args)
