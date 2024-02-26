import pytest
import sqlite3
from unittest.mock import patch, Mock
from app.services.player_service import (
    create_player,
    get_player,
    update_player,
    delete_player
)


@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.close()


PLAYER = {
    "first_name": "Abel",
    "last_name": "Spithost",
    "date_of_birth": "1992-08-11",
    "position": "D",
    "shoots": "L"
}
PLAYER_LIST_VALUES = ["Abel", "Spithost", "1992-08-11", "D", "L", None, None, None]


def test_create_player_success(in_memory_db):
    with patch('app.services.player_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.player_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            create_player(PLAYER)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                       INSERT INTO "players"
                       ("first_name", "last_name", "date_of_birth", "position", "shoots", "profile_picture", "middle_name", "nickname")
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''',
                       PLAYER_LIST_VALUES
            )


def test_create_player_failure(in_memory_db):
    with patch('app.services.player_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.player_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                create_player(PLAYER)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                       INSERT INTO "players"
                       ("first_name", "last_name", "date_of_birth", "position", "shoots", "profile_picture", "middle_name", "nickname")
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''',
                       ["Abel", "Spithost", "1992-08-11", "D", "L", None, None, None]
            )


def test_get_player_success(in_memory_db):
    with patch('app.services.player_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.player_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor
            mock_response = Mock()
            mock_response.fetchone.return_value = PLAYER
            mock_cursor.execute.return_value = mock_response

            response = get_player(1)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                             SELECT *
                             FROM "players"
                             WHERE "id" = ?
                             ''', (1,)
            )
            assert response == dict(mock_response.fetchone.return_value)


def test_get_player_failure(in_memory_db):
    with patch('app.services.player_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.player_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                get_player(1)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                             SELECT *
                             FROM "players"
                             WHERE "id" = ?
                             ''',
                             (1,)
            )


def test_update_player_success(in_memory_db):
    with patch('app.services.player_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.player_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            response = update_player(1, PLAYER)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                       UPDATE "players"
                       SET "first_name" = ?, "last_name" = ?, "date_of_birth" = ?, "position" = ?, "shoots" = ?, "profile_picture" = ?, "middle_name" = ?, "nickname" = ?
                       WHERE "id" = ?
                       ''',
                       PLAYER_LIST_VALUES + [1]
            )
            assert response == True


def test_update_player_failure(in_memory_db):
    with patch('app.services.player_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.player_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                update_player(1, PLAYER)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                       UPDATE "players"
                       SET "first_name" = ?, "last_name" = ?, "date_of_birth" = ?, "position" = ?, "shoots" = ?, "profile_picture" = ?, "middle_name" = ?, "nickname" = ?
                       WHERE "id" = ?
                       ''',
                       PLAYER_LIST_VALUES + [1]
            )



def test_delete_club_success(in_memory_db):
    with patch('app.services.player_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.player_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            response = delete_player(1)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                       DELETE FROM "players"
                       WHERE "id" = ?
                       ''', 
                       (1,)
            )
            assert response == True


def test_delete_club_failure(in_memory_db):
    with patch('app.services.player_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.player_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                delete_player(1)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                       DELETE FROM "players"
                       WHERE "id" = ?
                       ''', 
                       (1,)
            )
