import collections
import itertools
import numbers
import redis


class RedisNode(object):
    """Redis node class using `redis.StrictRedis`.
    
    """

    __slots__ = '_client', '_config',

    def __init__(self, host='localhost', port=6379,
                 **config):
        if not isinstance(host, basestring):
            raise TypeError('`host` must be of `basestring`')
        if not isinstance(port, numbers.Integral):
            raise TypeError('`port` must be of `numbers.Integral`')
        config.update({
            'host': host,
            'port': port,
        })
        self._config = config
        self._client = redis.StrictRedis(**config)

    @property
    def host(self):
        return self._config['host']

    @property
    def port(self):
        return self._config['port']

    @property
    def client(self):
        return self._client

    def execute(self, command, *args, **kwargs):
        f = getattr(self.client, command)
        return f(*args, **kwargs)


class RedisBlock(object):
    """Redis block that is composited with `RedisNode`.
    
    """

    __slots__ = '_nodes', '_n_of_nodes', '_nodes_cycle',

    def __init__(self, nodes):
        if isinstance(nodes, list):
            nodes = dict(('node_%d' % i, node) for i, node in enumerate(nodes))
        elif not isinstance(nodes, collections.Mapping):
            raise TypeError(
                '`nodes` must be of `list` or `collections.Mapping`')
        self._nodes = nodes
        self._n_of_nodes = len(nodes)
        self._nodes_cycle = itertools.cycle(nodes.iteritems())

    def _get_node_by_rotation(self, with_name=True):
        name, node = self._nodes_cycle.next()
        if with_name:
            return name, node
        return node

    def execute(self, command, *args, **kwargs):
        name, node = self._get_node_by_rotation()
        return node.execute(command, *args, **kwargs)


class Redispace(object):
    """Shards data into ``RedisBlock`s and distributes operations to
    ``RedisNode``s.
    
    """
