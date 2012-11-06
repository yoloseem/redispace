from attest import Tests, assert_hook
from redispace.replication import RedisReplication
from redispace.sharding import RedisRing
from redis import StrictRedis


suite = Tests()


@suite.test
def hashring_test():
    a, b, c, d = (RedisReplication([StrictRedis()]) for e in range(4))
    ring = RedisRing([a, b, c, d])
    assert ring.get_node_by_key('a') != ring.get_node_by_key('b')
    assert ring.get_node_by_key('b') != ring.get_node_by_key('c')
