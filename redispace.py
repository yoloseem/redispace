""":mod:`redispace` --- redispace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

redispace is a `Redis`_ client based on `redis-py`_.

.. _Redis: http://redis.io/
.. _redis-py: https://github.com/andymccurdy/redis-py

"""

import collections
import itertools
import numbers
import redis


__slots__ = ('RedisNode', 'RedisBlock', 'RedisCluster', )


class RedisNode(object):
    """Redis node class using :class:`redis.StrictRedis`.
    
    """

    __slots__ = '_client', '_config',

    def __init__(self, host='localhost', port=6379,
                 **config):
        """

        :param host: host of redis server
        :type host: :class:`basestring`
        :param port: port of redis server
        :type port: :class:`numbers.Integral`

        """
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
        """Read-only attribute to get host of bound redis.

        :returns: the host of bound redis server
        :rtype: :class:`basestring`

        """
        return self._config['host']

    @property
    def port(self):
        """Read-only attribute to get port of bound redis.

        :returns: the port of bound redis server
        :rtype: :class:`numbers.Integral`

        """
        return self._config['port']

    @property
    def client(self):
        """Read-only attribute to get the redis client bound to self.

        :returns: the redis client that is bound to self.
        :rtype: :class:`redis.StrictRedis`

        """
        return self._client

    def execute(self, command, *args, **kwargs):
        """Proxy for method of :attr:`RedisNode.client`.
        
        .. sourcecode:: python

           node = RedisNode()
           result = node.execute('set', 'key', 'value')
           value = node.execute('get', 'key')

           # is equivalent to:

           result = node.client.set('key', 'value')
           value = node.client.get('key')

        :param command: the name of :attr:`RedisNode.client`'s method to call
        :type command: :class:`basestring`

        """
        f = getattr(self.client, command)
        return f(*args, **kwargs)


class RedisBlock(object):
    """Redis block that is composited with :class:`RedisNode`.

    :param nodes: the collection of :class:`RedisNode`
    :type nodes: :class:`collections.Mapping` or :class:`list`

    If :class:`list` is given for :data:`nodes`, it converts the list to
    :class:`dict` internally.
    
    """

    __slots__ = '_nodes', '_nodes_cycle',

    def __init__(self, nodes):
        if isinstance(nodes, list):
            nodes = dict(('node_%d' % i, node) for i, node in enumerate(nodes))
        elif not isinstance(nodes, collections.Mapping):
            raise TypeError(
                '`nodes` must be of `collections.Mapping` or `list`')
        self._nodes = nodes
        self._nodes_cycle = itertools.cycle(nodes.iteritems())

    def get_node_by_rotation(self, with_name=True):
        """Pooling :class:`RedisNode` and fetch one in turn.

        .. sourcecode:: pycon

           >>> rb.get_node_by_rotation()
           ('node_1', <redispace.RedisNode object at 0x1376990>)
           >>> rb.get_node_by_rotation()
           ('node_0', <redispace.RedisNode object at 0x1376810>)
           >>> rb.get_node_by_rotation()
           ('node_1', <redispace.RedisNode object at 0x1376990>)
           >>> rb.get_node_by_rotation()
           ('node_0', <redispace.RedisNode object at 0x1376810>)

        :param with_name: the boolean value whether this method returns node
                          with its name or not
        :type with_name: :class:`bool`
        :returns: the redis node that is in its turn
        :rtype: :class:`tuple` or :class:`RedisNode`

        """
        name, node = self._nodes_cycle.next()
        if with_name:
            return name, node
        return node

    def execute(self, command, *args, **kwargs):
        """Proxy for method of :attr:`RedisBlock.client`.::

        Same as :meth:`RedisNode.execute`.

        :param command: the name of :attr:`RedisBlock.client`'s method to call
        :type command: :class:`basestring`

        """
        name, node = self.get_node_by_rotation()
        return node.execute(command, *args, **kwargs)


class Redispace(object):
    """Shards data into :class:`RedisBlock` and distributes operations to
    :class:`RedisNode`.
    
    """
