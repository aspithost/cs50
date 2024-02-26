from app.helpers.list import validate_list_keys

LIST_KEYS = ["one", "two", "three"]

def test_validate_list_keys():
    assert validate_list_keys(["one"], LIST_KEYS) == True
    assert validate_list_keys(["two", "three"], LIST_KEYS) == True
    assert validate_list_keys(["one", "two", "three"], LIST_KEYS) == True
    assert validate_list_keys(["test"], LIST_KEYS) == False
    assert validate_list_keys([], LIST_KEYS) == False
    assert validate_list_keys({}, LIST_KEYS) == False
    assert validate_list_keys([1, "!"], LIST_KEYS) == False
    assert validate_list_keys({"one": "test"}, LIST_KEYS) == False