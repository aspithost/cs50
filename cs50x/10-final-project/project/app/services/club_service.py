import logging
import sqlite3
from app.constants.clubs import CLUB_KEYS, COLORS_KEYS, DETAILS_KEYS
from app.db import get_football_db_conn, get_cursor
from app.helpers.dict import format_dict
from app.helpers.dict import dict_to_list_values


def create_club(club):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.execute('INSERT INTO "clubs" ("name") VALUES (?)', (club["name"],))
        conn.commit()
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def get_club(club_id, options):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.row_factory = sqlite3.Row
        colors = options["colors"]
        details = options["details"]
        if colors and details:
            res = cursor.execute('''
                                SELECT *
                                FROM "clubs"
                                LEFT JOIN "club_colors" ON "club_colors"."club_id" = "clubs"."id"
                                LEFT JOIN "club_details" ON "club_details"."club_id" = "clubs"."id"
                                WHERE "clubs"."id" = ?''', (club_id,))
        elif colors:
            res = cursor.execute('''
                                SELECT *
                                FROM "clubs"
                                LEFT JOIN "club_colors" ON "club_colors"."club_id" = "clubs"."id"
                                WHERE "clubs"."id" = ?''', (club_id,))
        elif details:
            res = cursor.execute('''
                                SELECT *
                                FROM "clubs"
                                LEFT JOIN "club_details" ON "club_details"."club_id" = "clubs"."id"
                                WHERE "clubs"."id" = ?''', (club_id,))
        else:
            res = cursor.execute('''
                                SELECT *
                                FROM "clubs"
                                WHERE "clubs"."id" = ?''', (club_id,))
        try:
            data = dict(res.fetchone())
        except TypeError:
            return None
        if colors or details:
            del data["club_id"]
        if colors:
            data = format_dict(data, COLORS_KEYS, "colors")
        if details:
            data = format_dict(data, DETAILS_KEYS, "details")
        return data
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def update_club(club_id, club):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        values = dict_to_list_values(club, CLUB_KEYS) + [club_id]
        cursor.execute('UPDATE "clubs" SET "name" = ? AND "logo" = ? WHERE "id" = ?', values)
        conn.commit()
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def delete_club(club_id):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.execute('DELETE FROM "clubs" WHERE "id" = ?', (club_id,))
        conn.commit()
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def create_club_colors(club_id, club_colors):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        values = [club_id] + dict_to_list_values(club_colors, COLORS_KEYS)
        cursor.execute('''
                       INSERT INTO "club_colors"
                       ("club_id", "shirt_primary", "shirt_secondary", "shirt_pattern", "shorts", "socks")
                       VALUES (?, ?, ?, ?, ?, ?)''',
                       values)
        conn.commit()
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def update_club_colors(club_id, club_colors):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        list_values = dict_to_list_values(club_colors, COLORS_KEYS)
        list_values.append(club_id)
        cursor.execute('''
                       UPDATE "club_colors"
                       SET "shirt_primary" = ?, "shirt_secondary" = ?, "shirt_pattern" = ?, "shorts" = ?, "socks" = ?
                       WHERE "club_id" = ?
                       ''',
                       list_values)
        conn.commit()
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def create_club_details(club_id, club_details):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        values = [club_id] + dict_to_list_values(club_details, DETAILS_KEYS)
        cursor.execute('''
                       INSERT INTO "club_details"
                       ("club_id", "city", "country", "street_address", "postal_code", "founded")
                       VALUES (?, ?, ?, ?, ?, ?)''',
                       values)
        conn.commit()
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def update_club_details(club_id, club_details):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        list_values = dict_to_list_values(club_details, DETAILS_KEYS)
        list_values.append(club_id)
        cursor.execute('''
                       UPDATE "club_details"
                       SET "city" = ?, "country" = ?, "street_address" = ?, "postal_code" = ?, "founded" = ?
                       WHERE "club_id" = ?
                       ''',
                       list_values)
        conn.commit()
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()
