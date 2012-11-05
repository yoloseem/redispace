from attest import Tests, assert_hook
from redispace.protocol import RedisProtocol


suite = Tests()


class RedisDict(RedisProtocol):
    
    client = None

    def __init__(self, dict_={}):
        super(RedisDict, self).__init__()
        self.client = dict_

    def execute_command(self, command, *args, **options):
        if command == 'get':
            k = args[0]
            return self.client[k]
        elif command == 'set':
            k, v = args[0], args[1]
            self.client[k] = v
            return 1
        else:
            NotImplemented


@suite.test
def commands_test():
    rd = RedisDict()
    rd.set('key', 'value')
    assert rd.get('key') == 'value'
