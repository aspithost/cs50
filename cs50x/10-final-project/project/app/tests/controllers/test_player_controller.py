import pytest
from unittest.mock import patch
from app import app
from app.constants.errors import ERROR_400, ERROR_404_PLAYERS


PLAYER = {
    "first_name": "Abel",
    "last_name": "Spithost",
    "date_of_birth": "1992-08-11",
    "position": "D",
    "shoots": "L"
}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("app.controllers.player_controller.create_player")
def test_create_player_route_success(mock_create_player, client):
    mock_create_player.return_value = PLAYER

    response = client.post("/players", json={"player": PLAYER})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Player created successfully!"


def test_create_player_route_invalid(client):
    response = client.post("/players", json={"player": {"invalid_key": "Not a football player"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.player_controller.get_player")
def test_get_player_route_success(mock_get_player, client):
    mock_get_player.return_value = PLAYER

    response = client.get("/players/1")

    assert response.status_code == 200
    assert response.get_json() == PLAYER


@patch("app.controllers.player_controller.get_player")
def test_get_player_route_not_found(mock_get_player, client):
    mock_get_player.return_value = None

    response = client.get("/players/1")

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_PLAYERS


@patch("app.controllers.player_controller.update_player")
def test_update_player_route_success(mock_update_player, client):
    mock_update_player.return_value = (True, None)

    response = client.put("/players/1", json={"player": PLAYER})

    assert response.status_code == 201
    assert response.get_json()["player"] == PLAYER


def test_update_player_route_invalid(client):
    response = client.put("/players/1", json={"player": {"invalid_key": "hockey player"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.player_controller.update_player")
def test_update_player_route_not_found(mock_update_player, client):
    mock_update_player.return_value = False

    response = client.put("/players/1", json={"player": PLAYER})

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_PLAYERS


@patch("app.controllers.player_controller.delete_player")
def test_delete_player_route_success(mock_delete_player, client):
    mock_delete_player.return_value = True

    response = client.delete("/players/1")

    assert response.status_code == 204
    assert not response.get_data()


@patch("app.controllers.player_controller.delete_player")
def test_delete_player_route_not_found(mock_delete_player, client):
    mock_delete_player.return_value = False

    response = client.delete("/players/1")

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_PLAYERS
