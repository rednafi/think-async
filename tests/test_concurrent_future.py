from unittest.mock import patch

import patterns.concurrent_future as main


@patch("patterns.concurrent_future.time.sleep", autospec=True)
def test_foo(mock_time_sleep, capsys):
    task_id = "42"

    # Call 'foo'.
    main.foo(task_id=task_id)

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert f"task-id: {task_id}, status: done" in out
    mock_time_sleep.assert_called_once()


@patch.object(main, "MAX_CONCURRENCY", 2)
@patch.object(main, "N_TASKS", 2)
@patch("patterns.concurrent_future.time.sleep", autospec=True)
def test_threads_with_executor_submit(mock_time_sleep, capsys):

    # Call 'threads_with_executor_submit'.
    main.threads_with_executor_submit()

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Doing it with thread submit" in out
    assert mock_time_sleep.call_count == 2


@patch.object(main, "MAX_CONCURRENCY", 2)
@patch.object(main, "N_TASKS", 2)
@patch("patterns.concurrent_future.time.sleep", autospec=True)
def test_threads_with_executor_map(mock_time_sleep, capsys):

    # Call 'threads_with_executor_map'.
    main.threads_with_executor_map()

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Doing it with thread map" in out
    assert mock_time_sleep.call_count == 2


@patch.object(main, "MAX_CONCURRENCY", 2)
@patch.object(main, "N_TASKS", 2)
@patch("patterns.concurrent_future.time.sleep", autospec=True)
def test_processes_with_executor_submit(mock_time_sleep, capsys):

    # Call 'processes_with_executor_submit'.
    main.processes_with_executor_submit()

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Doing it with process submit" in out
    assert mock_time_sleep.call_count == 2


@patch.object(main, "MAX_CONCURRENCY", 2)
@patch.object(main, "N_TASKS", 2)
@patch("patterns.concurrent_future.time.sleep", autospec=True)
def test_processes_with_executor_map(mock_time_sleep, capsys):

    # Call 'processes_with_executor_map'.
    main.processes_with_executor_map()

    # Assert.
    out, err = capsys.readouterr()
    assert err == ""
    assert "Doing it with process map" in out
    assert mock_time_sleep.call_count == 0  # Mock can't see the func call here.
