""":mod:`redispace.replication` Redis replication wrapper.

"""
import redis
from .protocol import RedisProtocol


class RedisReplication(RedisProtocol):
    pass
