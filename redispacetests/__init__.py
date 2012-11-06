from attest import Tests
from . import protocol, replication


suite = Tests()
suite.register(protocol.suite)
suite.register(replication.suite)


@suite.test
def boolean():
    assert True is not False
