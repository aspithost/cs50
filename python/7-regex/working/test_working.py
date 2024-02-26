from working import convert
from pytest import raises


def test_happy():
    assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"
    assert convert("9 AM to 5 PM") == "09:00 to 17:00"
    assert convert("12:00 AM to 12:00 PM") == "00:00 to 12:00"
    assert convert("12 PM to 12 AM") == "12:00 to 00:00"


def test_unhappy():
    with raises(ValueError):
        convert("9 AM 10 PM")
    with raises(ValueError):
        convert("13:00 AM to 13:00 PM")
    with raises(ValueError):
        convert("AB AM to CD PM")