from attest import Tests


tests = Tests()


@tests.test
def dummy():
    assert True == True


if __name__ == '__main__':
    tests.run()
