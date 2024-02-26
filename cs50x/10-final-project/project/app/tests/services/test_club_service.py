import pytest
import sqlite3
from unittest.mock import patch, Mock
from app.services.club_service import (
    create_club,
    get_club,
    update_club,
    delete_club,
    create_club_colors,
    update_club_colors,
    create_club_details,
    update_club_details
)


@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.close()


CLUB = {"name": "v.v. Potetos"}


def test_create_club_success(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            create_club(CLUB)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'INSERT INTO "clubs" ("name") VALUES (?)', (CLUB["name"],)
            )


def test_create_club_failure(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                create_club(CLUB)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'INSERT INTO "clubs" ("name") VALUES (?)', (CLUB["name"],)
            )


def test_get_club_success(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor
            mock_response = Mock()
            mock_response.fetchone.return_value = {"test": 123}
            mock_cursor.execute.return_value = mock_response

            response = get_club(1, {"colors": None, "details": None})

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                                SELECT *
                                FROM "clubs"
                                WHERE "clubs"."id" = ?''', (1,)
            )
            assert response == mock_response.fetchone.return_value


def test_get_club_failure(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                get_club(1, {"colors": None, "details": None})

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                                SELECT *
                                FROM "clubs"
                                WHERE "clubs"."id" = ?''', (1,)
            )


def test_update_club_success(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            response = update_club(1, CLUB)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'UPDATE "clubs" SET "name" = ? AND "logo" = ? WHERE "id" = ?', [CLUB["name"], None, 1],
            )
            assert response == True


def test_update_club_failure(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                update_club(1, CLUB)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'UPDATE "clubs" SET "name" = ? AND "logo" = ? WHERE "id" = ?', [CLUB["name"], None, 1],
            )


def test_delete_club_success(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            response = delete_club(1)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'DELETE FROM "clubs" WHERE "id" = ?', (1,),
            )
            assert response == True


def test_delete_club_failure(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                delete_club(1)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'DELETE FROM "clubs" WHERE "id" = ?', (1,),
            )


COLORS = {
    "shirt_primary": "green",
    "shirt_secondary": "white",
    "shirt_pattern": "bars_vertical_single",
    "shorts": "white",
    "socks": "green"
}


def test_create_club_colors_success(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            create_club_colors(1, COLORS)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                    '''
                       INSERT INTO "club_colors"
                       ("club_id", "shirt_primary", "shirt_secondary", "shirt_pattern", "shorts", "socks")
                       VALUES (?, ?, ?, ?, ?, ?)''',
                       [1, "green", "white", "bars_vertical_single", "white", "green"]
            )


def test_create_club_colors_failure(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                create_club_colors(1, COLORS)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                    '''
                       INSERT INTO "club_colors"
                       ("club_id", "shirt_primary", "shirt_secondary", "shirt_pattern", "shorts", "socks")
                       VALUES (?, ?, ?, ?, ?, ?)''',
                       [1, "green", "white", "bars_vertical_single", "white", "green"]
            )


def test_update_club_colors_success(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            response = update_club_colors(1, COLORS)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                    '''
                       UPDATE "club_colors"
                       SET "shirt_primary" = ?, "shirt_secondary" = ?, "shirt_pattern" = ?, "shorts" = ?, "socks" = ?
                       WHERE "club_id" = ?
                       ''',
                       ["green", "white", "bars_vertical_single", "white", "green", 1]
            )
            assert response == True


def test_update_club_colors_failure(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                update_club_colors(1, COLORS)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                    '''
                       UPDATE "club_colors"
                       SET "shirt_primary" = ?, "shirt_secondary" = ?, "shirt_pattern" = ?, "shorts" = ?, "socks" = ?
                       WHERE "club_id" = ?
                       ''',
                       ["green", "white", "bars_vertical_single", "white", "green", 1]
            )


DETAILS = {
    "city": "Groningen",
    "country": "NLD"
}


def test_create_club_details_success(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            create_club_details(1, DETAILS)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                    '''
                       INSERT INTO "club_details"
                       ("club_id", "city", "country", "street_address", "postal_code", "founded")
                       VALUES (?, ?, ?, ?, ?, ?)''',
                       [1, "Groningen", "NLD", None, None, None]
            )


def test_create_club_details_failure(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                create_club_details(1, DETAILS)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                    '''
                       INSERT INTO "club_details"
                       ("club_id", "city", "country", "street_address", "postal_code", "founded")
                       VALUES (?, ?, ?, ?, ?, ?)''',
                       [1, "Groningen", "NLD", None, None, None]
            )


def test_update_club_details_success(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            response = update_club_details(1, DETAILS)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                    '''
                       UPDATE "club_details"
                       SET "city" = ?, "country" = ?, "street_address" = ?, "postal_code" = ?, "founded" = ?
                       WHERE "club_id" = ?
                       ''',
                       ["Groningen", "NLD", None, None, None, 1]
            )
            assert response == True


def test_update_club_details_failure(in_memory_db):
    with patch('app.services.club_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.club_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                update_club_details(1, DETAILS)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                    '''
                       UPDATE "club_details"
                       SET "city" = ?, "country" = ?, "street_address" = ?, "postal_code" = ?, "founded" = ?
                       WHERE "club_id" = ?
                       ''',
                       ["Groningen", "NLD", None, None, None, 1]
            )