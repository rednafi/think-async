from twisted.internet import defer, reactor


def get_dummy_number(
    input_number: int, defer_duration: float = 2, multiplier: float = 3
) -> defer.Deferred:
    """
    This function is a dummy which simulates a delayed result and
    returns a Deferred which will fire with that result.
    """

    print("get_dummy_number called")

    deferred = defer.Deferred()
    # Simulate a delayed result by asking the reactor to fire the
    # Deferred in '2 seconds' time with the result 'input_number * 3'.
    reactor.callLater(defer_duration, deferred.callback, input_number * multiplier)
    return deferred


def cb_print_number(result: int) -> None:
    """
    Data handling function to be added as a callback: handles the
    data by printing the result
    """
    print(f"Result received: {result}")


def orchestrator(stop_after: float = 4) -> None:
    deferred = get_dummy_number(3)
    deferred.addCallback(cb_print_number)

    # Manually set up the end of the process by asking the reactor to
    # stop itself in 4 seconds time.
    reactor.callLater(stop_after, reactor.stop)

    # Start up the Twisted reactor (event loop handler) manually.
    print("Starting the reactor")
    reactor.run()


if __name__ == "__main__":
    orchestrator()
