from attest import Tests


tests = Tests()


@tests.test
def dummy():
    assert True == False


if __name__ == '__main__':
    tests.run()
