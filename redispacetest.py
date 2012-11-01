from attest import Tests


tests = Tests()


@tests.test
def redisblock():
    from redispace import RedisBlock, RedisNode
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


if __name__ == '__main__':
    tests.run()
