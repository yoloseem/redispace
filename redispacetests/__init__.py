from attest import Tests
from . import protocol, replication


suite = Tests()
suite.register(protocol.suite)
suite.register(replication.suite)


@suite.test
def version():
    import redispace
    assert redispace.VERSION == '0.1.1'
