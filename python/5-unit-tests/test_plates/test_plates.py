from plates import is_valid

def test_numbers():
    assert is_valid("20") == False
    assert is_valid("AB20") == True
    assert is_valid("AB02") == False
    assert is_valid("AB20C") == False


def test_length():
    assert is_valid("A") == False
    assert is_valid("ABCDEF") == True
    assert is_valid("ABCDEFG") == False


def test_alphanumeric():
    assert is_valid("AB??") == False
