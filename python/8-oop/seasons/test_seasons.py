from seasons import get_date, calc_minutes
import datetime
import pytest


def test_date_happy():
    assert get_date("2011-11-11") == datetime.date(2011, 11, 11)
    assert get_date("2024-11-11") == datetime.date(2024, 11, 11)


def test_date_unhappy():
    with pytest.raises(SystemExit):
        get_date("20111-11-11")
    with pytest.raises(SystemExit):
        get_date("2011-13-13")
    with pytest.raises(SystemExit):
        get_date("20111-11-11-11")


def test_minutes_happy():
    assert calc_minutes(datetime.date(2000, 1, 2), datetime.date(2000, 1, 1)) == "One thousand, four hundred forty minutes"
    assert calc_minutes(datetime.date(2024, 1, 1), datetime.date(2024, 1, 2)) == "Minus one thousand, four hundred forty minutes"