import logging
import sqlite3
from app.db import get_football_db_conn, get_cursor
from app.helpers.dict import dict_to_list_values
from app.constants.players import PLAYER_KEYS


def create_player(player):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        values = dict_to_list_values(player, PLAYER_KEYS)
        cursor.execute('''
                       INSERT INTO "players"
                       ("first_name", "last_name", "date_of_birth", "position", "shoots", "profile_picture", "middle_name", "nickname")
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       ''',
                       values)
        conn.commit()
    except (sqlite3.Error, KeyError) as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def get_player(player_id):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.row_factory = sqlite3.Row
        res = cursor.execute('''
                             SELECT *
                             FROM "players"
                             WHERE "id" = ?
                             ''',
                             (player_id,))
        player = res.fetchone()
        try:
            return dict(player) if player else None
        except TypeError:
            return None
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def update_player(player_id, player):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        list_values = dict_to_list_values(player, PLAYER_KEYS)
        list_values.append(player_id)
        cursor.execute('''
                       UPDATE "players"
                       SET "first_name" = ?, "last_name" = ?, "date_of_birth" = ?, "position" = ?, "shoots" = ?, "profile_picture" = ?, "middle_name" = ?, "nickname" = ?
                       WHERE "id" = ?
                       ''',
                        list_values
        )
        conn.commit()
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def delete_player(player_id):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.execute('''
                       DELETE FROM "players"
                       WHERE "id" = ?
                       ''',
                       (player_id,))
        conn.commit()
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()