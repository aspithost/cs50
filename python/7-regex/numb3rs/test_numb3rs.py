from numb3rs import validate


def test_happy():
    assert validate("255.255.255.255") == True
    assert validate("255.255.0.0") == True
    assert validate("0.0.0.0") == True


def test_unhappy():
    assert validate("a.b.c.d") == False
    assert validate("/./././") == False
    assert validate("255.255.255") == False
    assert validate("255.255.255.255.0") == False
    assert validate("256.255.255.255") == False
    assert validate("255.256.256.256") == False