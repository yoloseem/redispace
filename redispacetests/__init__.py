from attest import Tests, assert_hook


suite = Tests()


@suite.test
def boolean():
    assert True is not False
