import pytest
from app.helpers.dict import validate_dict_keys, format_dict, format_dict_nested_keys, dict_to_list_values


FAKE_LIST = [1, "three", 2, "six"]


def test_validate_dict_keys():
    assert validate_dict_keys({1: "test", "three": "test"}, FAKE_LIST) == True
    assert validate_dict_keys({1: "test", "seven": "test"}, FAKE_LIST) == False
    assert validate_dict_keys([1, "three", 2, "six"], FAKE_LIST) == False
    assert validate_dict_keys([], FAKE_LIST) == False
    assert validate_dict_keys({}, FAKE_LIST) == False
    assert validate_dict_keys((), FAKE_LIST) == False


def test_format_dict():
    assert format_dict({2: "test", 4: "test"}, FAKE_LIST, "new_key") == {"new_key": {2: "test"}, 4: "test"}
    assert format_dict({"three": "test"}, FAKE_LIST, "some_key") == {"some_key": {"three":"test"}}
    assert format_dict({"test": "testie"}, FAKE_LIST, "new_key") == {"test": "testie"}
    assert format_dict({}, FAKE_LIST, "new_key") == {}
    assert format_dict([], FAKE_LIST, "new_key") == []
    assert format_dict((), FAKE_LIST, "new_key") == ()
    with pytest.raises(TypeError):
        format_dict([1], FAKE_LIST, "new_key")


def test_format_dict_nested_keys():
    assert format_dict_nested_keys({"name": "Abel", "age": 31}, ["age"], ["one", "two"]) == {"name": "Abel", "one": {"two": {"age": 31}}}
    assert format_dict_nested_keys({"one": 1, "nested": {"two": 2}}, ["one"], ["nested"]) == {"nested": {"one": 1, "two": 2}}
    assert format_dict_nested_keys({}, ["some"], ["test", "run"]) == {"test": {"run": {}}}
    with pytest.raises(TypeError):
        format_dict_nested_keys({"test": "one"})
        format_dict_nested_keys({"test": "one"}, ["test"])
    with pytest.raises(IndexError):
        format_dict_nested_keys({"test": "one"}, ["test"], [])
        format_dict_nested_keys({"test": "one"}, [], ["test"])
        format_dict_nested_keys([], [], [])
    with pytest.raises(AttributeError):
        format_dict_nested_keys([], ["some"], ["test", "run"])
        format_dict_nested_keys((), ["some"], ["test", "run"])


def test_dict_to_list_values():
    assert dict_to_list_values({1: "test", "six": "five"}, FAKE_LIST) == ["test", None, None, "five"]
    assert dict_to_list_values({"three": "U"}, FAKE_LIST) == [None, "U", None, None]
    assert dict_to_list_values({11: 12, 13:14}, FAKE_LIST) == [None, None, None, None]
    assert dict_to_list_values({}, FAKE_LIST) == [None, None, None, None]
    assert dict_to_list_values([], FAKE_LIST) == [None, None, None, None]
    assert dict_to_list_values((), FAKE_LIST) == [None, None, None, None]
    assert dict_to_list_values({"three": "U"}, {"one": "two"}) == [None]