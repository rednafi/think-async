from twisted.internet import reactor, defer


def get_dummy_data(input_data):
    """
    This function is a dummy which simulates a delayed result and
    returns a Deferred which will fire with that result. Don't try too
    hard to understand this.
    """
    print("get_dummy_data called")
    deferred = defer.Deferred()
    # simulate a delayed result by asking the reactor to fire the
    # Deferred in 2 seconds time with the result inputData * 3
    reactor.callLater(2, deferred.callback, input_data * 3)
    return deferred


def cb_print_data(result):
    """
    Data handling function to be added as a callback: handles the
    data by printing the result
    """
    print(f"Result received: {result}")


deferred = get_dummy_data(3)
deferred.addCallback(cb_print_data)

# manually set up the end of the process by asking the reactor to
# stop itself in 4 seconds time
reactor.callLater(4, reactor.stop)
# start up the Twisted reactor (event loop handler) manually
print("Starting the reactor")
reactor.run()
