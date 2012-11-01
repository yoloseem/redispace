from attest import TestBase, Tests, assert_hook, test
from redispace import *


class RedisBlockTest(TestBase):
   
    @test
    def get_node_by_rotation(self):
        nodes = [RedisNode(), RedisNode(), RedisNode()]
        rb = RedisBlock(nodes)
        assert rb.get_node_by_rotation() != rb.get_node_by_rotation()
        got_nodes = [
            rb.get_node_by_rotation(),
            rb.get_node_by_rotation(),
            rb.get_node_by_rotation(),
            rb.get_node_by_rotation(),
            rb.get_node_by_rotation(),
        ]
        assert got_nodes[0] == got_nodes[3]


suite = Tests([RedisBlockTest()])


if __name__ == '__main__':
    suite.run()
