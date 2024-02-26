import pytest
import sqlite3
from unittest.mock import patch, Mock
from app.services.team_service import (
    create_team,
    get_team,
    update_team,
    delete_team,
    create_team_member,
    get_team_members,
    delete_team_member,
)


@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.close()


TEAM = {
    "club_id": 1,
    "number": 3
}


def test_create_team_success(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            create_team(TEAM)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'INSERT INTO "teams" ("club_id", "number") VALUES (?, ?)', (TEAM["club_id"], TEAM["number"])
            )


def test_create_team_failure(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                create_team(TEAM)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'INSERT INTO "teams" ("club_id", "number") VALUES (?, ?)', (TEAM["club_id"], TEAM["number"])
            )


def test_get_team_success(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor
            mock_response = Mock()
            mock_response.fetchone.return_value = {"id": 1, "number": 7, "club_id": 1, "club_name": "v.v. Potetos"}
            mock_cursor.execute.return_value = mock_response

            response = get_team(1, {"colors": None, "details": None})

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                                 SELECT "teams"."id", "teams"."number", "teams"."club_id", "clubs"."name" AS "club_name"
                                 FROM "teams" 
                                 JOIN "clubs" ON "clubs"."id" = "teams"."club_id"
                                 WHERE "teams"."id" = ?''', (1,)
            )
            assert response == {
                "id": 1,
                "number": 7,
                "club": {
                    "id": 1,
                    "name": "v.v. Potetos"
                }
            }


def test_get_team_failure(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor
           
            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                get_team(1, {"colors": None, "details": None})

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                                 SELECT "teams"."id", "teams"."number", "teams"."club_id", "clubs"."name" AS "club_name"
                                 FROM "teams" 
                                 JOIN "clubs" ON "clubs"."id" = "teams"."club_id"
                                 WHERE "teams"."id" = ?''', (1,)
            )


def test_update_team_success(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            response = update_team(1, TEAM)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'UPDATE "teams" SET "club_id" = ? AND "number" = ?  WHERE "id" = ?',
                (TEAM["club_id"], TEAM["number"], 1),
            )
            assert response == True


def test_update_team_failure(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                update_team(1, TEAM)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'UPDATE "teams" SET "club_id" = ? AND "number" = ?  WHERE "id" = ?',
                (TEAM["club_id"], TEAM["number"], 1),
            )


def test_delete_team_success(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            response = delete_team(1)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'DELETE FROM "teams" WHERE "id" = ?', (1,),
            )
            assert response == True


def test_delete_team_failure(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                delete_team(1)

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                'DELETE FROM "teams" WHERE "id" = ?', (1,),
            )


def test_create_team_member_success(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            create_team_member(1, 2, ['22-23', '23-24'])

            mock_get_cursor.assert_called_once()
            mock_cursor.executemany.assert_called_once_with(
                '''
                       INSERT INTO "team_members" ("team_id", "player_id", "season")
                       VALUES (?, ?, ?)''',
                       ([(1, 2, '22-23'), (1, 2, '23-24')]),
            )


def test_create_team_member_failure(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.executemany.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                create_team_member(1, 2, ['22-23', '23-24'])

            mock_get_cursor.assert_called_once()
            mock_cursor.executemany.assert_called_once_with(
                '''
                       INSERT INTO "team_members" ("team_id", "player_id", "season")
                       VALUES (?, ?, ?)''',
                       ([(1, 2, '22-23'), (1, 2, '23-24')]),
            )


def test_get_team_members_success(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor
            mock_response = Mock()
            mock_response.fetchone.return_value = {"name": "v.v. Potetos", "number": 7}
            mock_response.fetchall.return_value = [
                {
                    "season": "22-23",
                    "date_of_birth": "1993-12-01",
                    "first_name": "Bart",
                    "id": 2,
                    "last_name": "Talens",
                    "middle_name": "Jelmer",
                    "nickname": None,
                    "position": "M",
                    "profile_picture": None,
                    "shoots": "R"
                },
                {
                    "season": "22-23",
                    "date_of_birth": "1992-08-11",
                    "first_name": "Abel",
                    "id": 3,
                    "last_name": "Spithost",
                    "middle_name": None,
                    "nickname": None,
                    "position": "D",
                    "profile_picture": None,
                    "shoots": "L"
                }
            ]
            mock_cursor.execute.return_value = mock_response

            response = get_team_members(1, ['22-23'])

            mock_get_cursor.assert_called_once()
            assert mock_cursor.execute.call_count == 2
            mock_cursor.execute.assert_any_call(
                '''
                                  SELECT "clubs"."name", "teams"."number"
                                  FROM "teams"
                                  JOIN "clubs" on "clubs"."id" = "teams"."club_id"
                                  WHERE "teams"."id" = ?
                                  ''', (1,)
            )
            mock_cursor.execute.assert_any_call(
                 '''
                                              SELECT "team_members"."season", "players".*
                                              FROM "team_members"
                                              JOIN "players" ON "players"."id" = "team_members"."player_id"
                                              WHERE "team_members"."team_id" = ?
                                              AND "team_members"."season" = ?
                                              ''',
                                              (1, '22-23')
            )

            assert response == {
                "name": "v.v. Potetos",
                "number": 7,
                "team_members": {
                    "22-23": [
                        {
                            "date_of_birth": "1993-12-01",
                            "first_name": "Bart",
                            "id": 2,
                            "last_name": "Talens",
                            "middle_name": "Jelmer",
                            "nickname": None,
                            "position": "M",
                            "profile_picture": None,
                            "shoots": "R"
                        },
                        {
                            "date_of_birth": "1992-08-11",
                            "first_name": "Abel",
                            "id": 3,
                            "last_name": "Spithost",
                            "middle_name": None,
                            "nickname": None,
                            "position": "D",
                            "profile_picture": None,
                            "shoots": "L"
                        }
                    ]
                }
            }



def test_get_team_members_failure(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.execute.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                get_team_members(1, ['22-23', '23-24'])

            mock_get_cursor.assert_called_once()
            mock_cursor.execute.assert_called_once_with(
                '''
                                  SELECT "clubs"."name", "teams"."number"
                                  FROM "teams"
                                  JOIN "clubs" on "clubs"."id" = "teams"."club_id"
                                  WHERE "teams"."id" = ?
                                  ''',
                                  (1,)
            )



def test_delete_team_member_success(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()    
            mock_get_cursor.return_value = mock_cursor

            response = delete_team_member(1, 2, ['22-23'])

            mock_get_cursor.assert_called_once()
            mock_cursor.executemany.assert_called_once_with(
                '''
                    DELETE FROM "team_members"
                    WHERE "team_id" = ?
                    AND "player_id" = ? 
                    AND "season" = ?''',
                    [(1, 2, '22-23')]
            )
            assert response == True


def test_delete_team_member_failure(in_memory_db):
    with patch('app.services.team_service.get_football_db_conn', return_value=in_memory_db):
        with patch('app.services.team_service.get_cursor') as mock_get_cursor:
            mock_cursor = Mock()    
            mock_get_cursor.return_value = mock_cursor

            mock_cursor.executemany.side_effect = sqlite3.Error("Simulated database error")

            with pytest.raises(sqlite3.Error):
                delete_team_member(1, 2, ['22-23'])
            
            mock_get_cursor.assert_called_once()
            mock_cursor.executemany.assert_called_once_with(
                '''
                    DELETE FROM "team_members"
                    WHERE "team_id" = ?
                    AND "player_id" = ? 
                    AND "season" = ?''',
                    [(1, 2, '22-23')]
            )