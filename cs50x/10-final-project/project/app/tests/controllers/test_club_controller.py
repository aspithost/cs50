import pytest
from unittest.mock import patch
from app import app
from app.constants.errors import ERROR_400, ERROR_404_CLUBS


CLUB = {
    "name": "v.v. Potetos",
    "logo": "some_blob"
}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("app.controllers.club_controller.create_club")
def test_create_club_route_success(mock_create_club, client):
    mock_create_club.return_value = CLUB

    response = client.post("/clubs", json={"club": CLUB})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Club created successfully!"


def test_create_club_route_invalid(client):
    response = client.post("/clubs", json={"club": {"invalid_key": "I am a team"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.club_controller.get_club")
def test_get_club_route_success(mock_get_club, client):
    mock_get_club.return_value = CLUB

    response = client.get("/clubs/1")

    assert response.status_code == 200
    assert response.get_json() == CLUB


@patch("app.controllers.club_controller.get_club")
def test_get_club_route_not_found(mock_get_club, client):
    mock_get_club.return_value = None

    response = client.get("/clubs/1")

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_CLUBS


@patch("app.controllers.club_controller.update_club")
def test_update_club_route_success(mock_update_club, client):
    mock_update_club.return_value = True

    response = client.put("/clubs/1", json={"club": CLUB})

    assert response.status_code == 201
    assert response.get_json()["club"] == CLUB


def test_update_club_route_invalid(client):
    response = client.put("/clubs/1", json={"hockey_rulesss": False})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


def test_update_club_route_invalid_two(client):
    response = client.put("/clubs/1", json={"club": {"stadium": "Yanmar stadion"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.club_controller.update_club")
def test_update_club_route_not_found(mock_update_club, client):
    mock_update_club.return_value = False

    response = client.put("/clubs/1", json={"club": CLUB})

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_CLUBS


@patch("app.controllers.club_controller.delete_club")
def test_delete_club_route_success(mock_delete_club, client):
    mock_delete_club.return_value = True

    response = client.delete("/clubs/1")

    assert response.status_code == 204
    assert not response.get_data()


@patch("app.controllers.club_controller.delete_club")
def test_delete_club_route_not_found(mock_delete_club, client):
    mock_delete_club.return_value = False

    response = client.delete("/clubs/1")

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_CLUBS


COLORS = {
    "shirt_primary": "green",
    "shirt_secondary": "white",
    "shirt_pattern": "bars_vertical_single",
    "shorts": "white",
    "socks": "green"
}


@patch("app.controllers.club_controller.create_club_colors")
def test_create_club_colors_success(mock_create_club, client):
    mock_create_club.return_value = COLORS

    response = client.post("/clubs/1/colors", json={"colors": COLORS})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Club colors created successfully!"


def test_update_club_route_invalid(client):
    response = client.put("/clubs/1/colors", json={"hockey_rulesss": False})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


def test_update_club_route_invalid_two(client):
    response = client.put("/clubs/1/colors", json={"colors": {"stadium": "Yanmar stadion"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.club_controller.update_club_colors")
def test_update_club_colors_route_success(mock_update_club, client):
    mock_update_club.return_value = True

    response = client.put("/clubs/1/colors", json={"colors": COLORS})

    assert response.status_code == 201
    assert response.get_json()["colors"] == COLORS


def test_update_club_colors_route_invalid(client):
    response = client.put("/clubs/1/colors", json={"hockey_rulesss": False})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


def test_update_club_colors_route_invalid_two(client):
    response = client.put("/clubs/1/colors", json={"club": {"stadium": "Yanmar stadion"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.club_controller.update_club_colors")
def test_update_club_colors_route_success(mock_update_club, client):
    mock_update_club.return_value = False

    response = client.put("/clubs/1/colors", json={"colors": COLORS})

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_CLUBS


DETAILS = {
    "city": "Groningen",
    "country": "NLD"
}


@patch("app.controllers.club_controller.create_club_details")
def test_create_club_details_success(mock_create_club, client):
    mock_create_club.return_value = DETAILS

    response = client.post("/clubs/1/details", json={"details": DETAILS})

    assert response.status_code == 201
    assert response.get_json()["message"] == "Club details created successfully!"


def test_update_club_route_invalid(client):
    response = client.put("/clubs/1/details", json={"hockey_rulesss": False})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


def test_update_club_route_invalid_two(client):
    response = client.put("/clubs/1/details", json={"details": {"stadium": "Yanmar stadion"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.club_controller.update_club_details")
def test_update_club_details_route_success(mock_update_club, client):
    mock_update_club.return_value = True

    response = client.put("/clubs/1/details", json={"details": DETAILS})

    assert response.status_code == 201
    assert response.get_json()["details"] == DETAILS


def test_update_club_details_route_invalid(client):
    response = client.put("/clubs/1/details", json={"hockey_rulesss": False})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


def test_update_club_details_route_invalid_two(client):
    response = client.put("/clubs/1/details", json={"club": {"stadium": "Yanmar stadion"}})

    assert response.status_code == 400
    assert response.get_json()["error"] == ERROR_400


@patch("app.controllers.club_controller.update_club_details")
def test_update_club_details_route_success(mock_update_club, client):
    mock_update_club.return_value = False

    response = client.put("/clubs/1/details", json={"details": DETAILS})

    assert response.status_code == 404
    assert response.get_json()["error"] == ERROR_404_CLUBS