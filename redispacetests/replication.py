from attest import Tests, assert_hook, raises
from redispace.replication import RedisReplication
from redis import StrictRedis


suite = Tests()


@suite.test
def nodes_cycle_test():
    with raises(TypeError):
        RedisReplication(1)
        RedisReplication([1])
    with raises(ValueError):
        RedisReplication([])
    r = RedisReplication([StrictRedis(), StrictRedis()])
    a, b, c, d = (r.get_node_by_rotation() for e in range(4))
    assert a == c and b == d and a != b
