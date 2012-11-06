""":mod:`redispace.replication` Redis replication wrapper.

"""
import collections
import itertools
import redis
from .protocol import RedisProtocol


class RedisReplication(RedisProtocol):
    """Redis client proxy that does pooling replica.

    """

    def __init__(self, nodes):
        super(RedisReplication, self).__init__()
        self.nodes = nodes

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        if isinstance(nodes, list):
            nodes = dict(('node_%d' % i, node) for i, node in enumerate(nodes))
        elif not isinstance(nodes, collections.Mapping):
            raise TypeError('`nodes` must be `collections.Mapping` or `list`.')
        if len(nodes) == 0:
            raise ValueError('`nodes` must contains at least one item.')
        for name, node in nodes.iteritems():
            if not isinstance(node, redis.StrictRedis):
                raise TypeError('`nodes` must be `collections.Mapping` that '\
                                'is composed of (`basestring`, '\
                                '`redis.StrictRedis`) pairs or `list` of '\
                                '`redis.StrictRedis`.')
        self._nodes = nodes
        self._nodes_cycle = itertools.cycle(nodes.iteritems())

    def get_node_by_rotation(self, with_name=True):
        name, node = self._nodes_cycle.next()
        return (name, node) if with_name else node

    def execute_command(self, command, *args, **options):
        name, node = self.get_node_by_rotation()
        f = getattr(node, command)
        return f(*args, **options)
