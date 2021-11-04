from unittest.mock import patch

import pytest
from twisted.internet import defer, reactor

import patterns.twisted_callback_hell as main


def test_get_dummy_number(capsys):
    # Call 'get_dummy_number'.
    main.get_dummy_number(input_number=10, defer_duration=0, multiplier=20)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "get_dummy_number called" in out


def test_cb_print_number(capsys):
    input_number = 11

    # Call 'cb_print_number'.
    main.cb_print_number(result=input_number)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert f"Result received: {input_number}" in out


@patch(
    "patterns.twisted_callback_hell.get_dummy_number",
    autospec=True,
    return_value=main.get_dummy_number(
        input_number=1,
        defer_duration=0.1,
        multiplier=2,
    ),
)
def test_orchestrator(mock_get_dummy_number, capsys):

    # Call 'orchestrator'.
    # On Python3.10, twisted raises:
    # DeprecationWarning: currentThread() is deprecated, use current_thread() instead
    with pytest.warns(None):
        main.orchestrator(stop_after=0.01)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Result received: 2" in out
    mock_get_dummy_number.assert_called_once()
