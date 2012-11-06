""":mod:`redispace.sharding` Redis sharding wrapper.

"""
import collections
import redis
from .protocol import RedisProtocol
from .replication import RedisReplication


class RedisRing(RedisProtocol):
    """Redis client proxy that does sharding data.

    """

    def __init__(self, nodes):
        super(RedisRing, self).__init__()
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
            if not isinstance(node, RedisReplication):
                raise TypeError('`nodes` must be `collections.Mapping` that '\
                                'is composed of (`basestring`, '\
                                '`redispace.replication.RedisReplication`) '\
                                'pairs or `list` of `RedisReplication`.')
        self._nodes = nodes
        self._nodes_list = list(self._nodes.iteritems())

    def get_node_by_key(self, key, with_name=True):
        name, node = self._nodes_list[hash(key) % len(self._nodes)]
        return (name, node) if with_name else node

    def execute_command(self, command, *args, **options):
        key = args[0] or options['key']
        name, node = self.get_node_by_key(key)
        f = getattr(node, command)
        return f(*args, **options)
