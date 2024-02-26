import pytest
from unittest.mock import patch
from app import app
from app.constants.errors import ERROR_400, ERROR_404_TEAMS, ERROR_404_TEAM_MEMBERS


TEAM = {
    "club_id": 1,
    "number": 3
}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("app.controllers.team_controller.create_team")
def test_create_team_route_success(mock_create_team, client):
    mock_create_team.return_value = TEAM

    response = client.post("/teams", json={"team": TEAM})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Team created successfully!"


def test_create_team_route_invalid(client):
    response = client.post("/teams", json={"team": {"invalid_key": "I am a team"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.team_controller.get_team")
def test_get_team_route_success(mock_get_team, client):
    mock_get_team.return_value = TEAM

    response = client.get("/teams/1")

    assert response.status_code == 200
    assert response.get_json() == TEAM


@patch("app.controllers.team_controller.get_team")
def test_get_team_route_not_found(mock_get_team, client):
    mock_get_team.return_value = None

    response = client.get("/teams/1")

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_TEAMS


@patch("app.controllers.team_controller.update_team")
def test_update_team_route_success(mock_update_team, client):
    mock_update_team.return_value = True

    response = client.put("/teams/1", json={"team": TEAM})

    assert response.status_code == 201
    assert response.get_json()["team"] == {**TEAM, "team_id": 1}


def test_update_team_route_invalid(client):
    response = client.put("/teams/1", json={"hockey_rulesss": False})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


def test_update_team_route_invalid_two(client):
    response = client.put("/teams/1", json={"team": {"stadium": "Yanmar stadion"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.team_controller.update_team")
def test_update_team_route_not_found(mock_update_team, client):
    mock_update_team.return_value = False

    response = client.put("/teams/1", json={"team": TEAM})

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_TEAMS


@patch("app.controllers.team_controller.delete_team")
def test_delete_team_route_success(mock_delete_team, client):
    mock_delete_team.return_value = True

    response = client.delete("/teams/1")

    assert response.status_code == 204
    assert not response.get_data()


@patch("app.controllers.team_controller.delete_team")
def test_delete_team_route_not_found(mock_delete_team, client):
    mock_delete_team.return_value = False

    response = client.delete("/teams/1")

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_TEAMS


TEAM_PLAYERS = {
    "name": "v.v. Potetos",
    "number": 7,
    "team_members": {
        "23-24": [
            {
                "id": 1,
                "date_of_birth": "1993-08-11",
                "first_name": "Abel",
                "middle_name": None,
                "last_name": "Spithost",
                "nickname": None,
                "position": "D",
                "shoots": "L",
                "profile_picture": None
            }
        ]
    }
}


@patch("app.controllers.team_controller.get_team_members")
def test_get_team_members_route_success(mock_get_team_members, client):
    mock_get_team_members.return_value = TEAM_PLAYERS

    response = client.get("/teams/1/players?seasons=23-24")

    assert response.status_code == 200
    assert response.get_json() == TEAM_PLAYERS


@patch("app.controllers.team_controller.get_team_members")
def test_get_team_members_route_not_found(mock_get_team_members, client):
    mock_get_team_members.return_value = None
    
    response = client.get("/teams/1/players?seasons=23-24")

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_TEAM_MEMBERS


@patch("app.controllers.team_controller.create_team_member")
def test_post_team_members_route_success(mock_create_team_member, client):
    mock_create_team_member.return_value = TEAM_PLAYERS

    response = client.post("/teams/1/players/1", json={"seasons": ["22-23", "23-24"]})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Team member added successfully!"


def test_post_team_members_route_invalid_one(client):
    response = client.post("/teams/1/players/1", json={"some_wrong_key": ["test"]})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


def test_post_team_members_route_invalid_two(client):
    response = client.post("/teams/1/players/1", json={"seasons": ["20-21"]})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.team_controller.delete_team_member")
def test_delete_team_member_route_success(mock_delete_team_member, client):
    mock_delete_team_member.return_value = True

    response = client.delete("/teams/1/players/1", json={"seasons": ["22-23"]})

    assert response.status_code == 204
    assert not response.get_data()


def test_delete_team_member_route_invalid_one(client):
    response = client.delete("/teams/1/players/1")

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


def test_delete_team_member_route_invalid_two(client):
    response = client.delete("/teams/1/players/1", json={"wrong_key": []})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.team_controller.delete_team_member")
def test_delete_team_member_route_not_found(mock_delete_team_member, client):
    mock_delete_team_member.return_value = False

    response = client.delete("/teams/1/players/1", json={"seasons": ["22-23"]})

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_TEAM_MEMBERS