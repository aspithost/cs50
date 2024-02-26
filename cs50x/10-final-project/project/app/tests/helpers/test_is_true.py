import pytest
from app.helpers.is_true import is_true


def test_is_true():
    assert is_true("true") == True
    assert is_true("True") == True
    assert is_true(" TRUE ") == True
    assert is_true("false") == False
    assert is_true("!true") == False
    assert is_true(123) == False