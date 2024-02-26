from project import format_filters, filter_players, filter_player, \
    filter_attribute, is_matching, format_player_value, sort_players, \
    format_keys, format_player_values, PLAYER_KEYS
import pytest
from types import SimpleNamespace


def test_format_filters():
    args = SimpleNamespace(
        name="Harry Kane", club="Tottenham Hotspur", position="Forward")
    assert format_filters(args, ["name", "club"]) == {"position": "Forward"}
    assert format_filters(args, ["name", "club", "goals"]) \
        == {"position": "Forward"}

    with pytest.raises(TypeError):
        format_filters(args)
    with pytest.raises(TypeError):
        format_filters("test")


def test_filter_players():
    fake_data = "full_name,position\nSergio Aguero,Forward\n"
    fake_csv_file = "./csv/pytest-fake-players.csv"
    with open(fake_csv_file, "w") as file:
        file.write(fake_data)

    first_result = filter_players(fake_csv_file, {"name": ["Sergio"]})
    second_result = filter_players(fake_csv_file, {"position": "Defender"})

    assert first_result == [
        {"full_name": "Sergio Aguero", "position": "Forward"}]
    assert second_result == []

    with pytest.raises(FileNotFoundError):
        filter_players("nonexistent_csv", {"some": "filter"})


def test_filter_player():
    favorite_striker = {
        "full_name": "Chris Wood",
        "goals_overall": "10",
        "Current Club": "Burnley",
        "appearances_overall": "38"
    }

    name_filter = {"name": ["Chris Wood"]}
    club_filter = {"club": ["Burnley"]}
    goal_filter = {"goals": ["9", "10"]}
    appearances_filter = {"appearances_overall": ["38"]}

    assert filter_player(favorite_striker, {}) == favorite_striker
    assert filter_player(favorite_striker, name_filter) == favorite_striker
    assert filter_player(favorite_striker, club_filter) == favorite_striker
    assert filter_player(favorite_striker, goal_filter) \
        == favorite_striker
    assert filter_player(favorite_striker, appearances_filter) \
        == favorite_striker
    assert filter_player(
        favorite_striker, {**name_filter, **club_filter}) \
        == favorite_striker
    assert filter_player(
        favorite_striker, {**name_filter, **club_filter, ** goal_filter}) \
        == favorite_striker
    assert filter_player(
        favorite_striker,
        {**name_filter, **club_filter, **goal_filter, **appearances_filter}) \
        == favorite_striker

    assert filter_player(
        favorite_striker, {"name": "Ashley Barnes"}) == None
    assert filter_player(
        favorite_striker, {**club_filter, "name": "Ashley Barnes"}) == None
    assert filter_player(
        favorite_striker,
        {**appearances_filter, "goals": [11, 12, 13]}) == None


# For non-list values, filter_attribute directly calls is_matching.
# Therefore, tests for those scenarios are covered in test_is_matching tests.
def test_filter_attribute():
    assert filter_attribute("Mohamed Salah", ["salah"]) == True
    assert filter_attribute("22", [21, 22, 23]) == True
    assert filter_attribute("defender", ["defender", "midfielder"]) == True

    assert filter_attribute("8", [9, 10]) == False
    assert filter_attribute("forward", ["goalkeeper", "defender"]) == False


def test_is_matching():
    assert is_matching("Liverpool", "liverpo") == True
    assert is_matching("Brighton & Hove Albion", "brighton") == True
    assert is_matching("Manchester City", "manchester city") == True
    assert is_matching("Manchester United", " manchester united ") == True
    assert is_matching("0", 0) == True
    assert is_matching("12", 12) == True

    assert is_matching("Brighton & Hove Albion", "brighton!") == False
    assert is_matching("Arsenal", "arsenal1") == False
    assert is_matching("Arsenal", "arsenal}") == False
    assert is_matching("1", 2) == False
    assert is_matching("9", 10) == False

    with pytest.raises(TypeError):
        is_matching(12, None)
    with pytest.raises(TypeError):
        is_matching("12", None)
    with pytest.raises(TypeError):
        is_matching(None, "Barnes")


def test_format_player_value():
    assert format_player_value({"goals_overall": "12"}, "goals") == 12
    assert format_player_value(
        {"nationality": "Dutch"}, "nationality") == "Dutch"

    with pytest.raises(KeyError):
        format_player_value({"goals_overall": "12"}, "test")
    with pytest.raises(KeyError):
        format_player_value({"full_name": "Thierry Henry"}, "club")


def test_sort_players():
    to_be_sorted = [
        {"goals_overall": "3"},
        {"goals_overall": "10"},
        {"goals_overall": "2"},
    ]

    assert sort_players(to_be_sorted, "goals", "descending") == [
        {"goals_overall": "10"},
        {"goals_overall": "3"},
        {"goals_overall": "2"},
    ]
    assert sort_players(to_be_sorted, "goals", "ascending") == [
        {"goals_overall": "2"},
        {"goals_overall": "3"},
        {"goals_overall": "10"},
    ]

    to_be_sorted_invalid = to_be_sorted[2]["goals_overall"] = 13
    with pytest.raises(KeyError):
        sort_players(to_be_sorted, "assists", "test")
    with pytest.raises(AttributeError):
        sort_players(to_be_sorted_invalid, "goals", "test")


def test_format_keys():
    assert format_keys(PLAYER_KEYS) == [
        "full_name", "Current Club", "appearances_overall", "goals_overall",
        "assists_overall", "position", "nationality"]


def test_format_player_values():
    players = [{"full_name": "Sergio Aguero", "age": 28},
               {"full_name": "Andy Robertson", "age": 22}]

    assert format_player_values(players, ["full_name"]) == [
        ["Sergio Aguero"], ["Andy Robertson"]
    ]

    with pytest.raises(KeyError):
        format_player_values(players, ["position"])
