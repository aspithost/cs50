from fuel import convert, gauge
import pytest


def test_convert():
    assert convert("1/3") == 33
    assert convert("3/4") == 75
    with pytest.raises(ValueError):
        convert("a/b")
    with pytest.raises(ValueError):
        convert("?/4")
    with pytest.raises(ValueError):
        convert("5/4")
    with pytest.raises(ZeroDivisionError):
        convert("4/0")


def test_gauge():
    assert gauge(0) == "E"
    assert gauge(1) == "E"
    assert gauge(40) == "40%"
    assert gauge(99) == "F"
    assert gauge(100) == "F"