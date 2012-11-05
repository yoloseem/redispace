""":mod:`redispace.protocol` Redis client protocol.

Implements the abstract redis client proxy. The protocol it implements follows
:class:`redis.StrictRedis`'s one.

"""

REDIS_COMMANDS = [
    'bgrewriteaof', 'bgsave', 'client_kill', 'client_list', 'config_get',
    'config_set', 'dbsize', 'time', 'debug_object', 'delete', 'echo',
    'flushall', 'flushdb', 'info', 'lastsave', 'object', 'ping', 'save',
    'shutdown', 'slaveof', 'append', 'getrange', 'bitcount', 'bitop', 'decr',
    'exists', 'expire', 'expireat', 'get', 'getbit', 'getset', 'incr',
    'incrbyfloat', 'mget', 'mset', 'msetnx', 'move', 'persist', 'pexpire',
    'pexpireat', 'pttl', 'randomkey', 'rename', 'renamenx', 'set', 'setbit',
    'setex', 'setnx', 'setrange', 'strlen', 'substr', 'ttl', 'type', 'watch',
    'unwatch', 'blpop', 'brpop', 'brpoplpush', 'lindex', 'linsert', 'llen',
    'lpop', 'lpush', 'lpushx', 'lrange', 'lrem', 'lset', 'ltrim', 'rpop',
    'rpoplpush', 'rpush', 'rpushx', 'sort', 'sadd', 'scard', 'sdiff',
    'sdiffstroe', 'sinter', 'sinterstore', 'sismember', 'smembers', 'smove',
    'spop', 'srandmember', 'srem', 'sunion', 'sunionstore', 'zadd', 'zcard',
    'zcount', 'zincrby', 'zinterstore', 'zrange', 'zrangebyscore', 'zrank',
    'zrem', 'zremrangebyrank', 'zremrangebyscore', 'zrevrange',
    'zrevrangebyscore', 'zrevrank', 'zscore', 'zunionstore', 'hdel', 'hexists',
    'hget', 'hgetall', 'hgetall', 'hincrby', 'hincrbyfloat', 'hkeys', 'hlen',
    'hset', 'hsetnx', 'hmset', 'hmget', 'hvals', 'publish', 'eval', 'evalsha',
    'script_exists', 'script_flush', 'script_kill', 'script_load',
    'register_script',
]


class RedisProtocol(object):

    def __init__(self):
        self._register_commands()

    def _register_commands(self):
        for command in REDIS_COMMANDS:
            f = (lambda c: lambda *args, **options: \
                           self.execute_command(c, *args, **options))(command)
            setattr(self, command, f)

    def execute_command(self, command, *args, **options):
        NotImplemented
