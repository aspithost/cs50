from bank import value


def test_hello():
    assert value("hello") == 0
    assert value("hello, there") == 0
    assert value("HEllo, TEST") == 0


def test_whitespace():
    assert value("   hello ") == 0
    assert value("hello   ") == 0
    assert value("  hey ") == 20


def test_h():
    assert value("howdy") == 20
    assert value("HIII") == 20


def test_wrong():
    assert value("greetings") == 100