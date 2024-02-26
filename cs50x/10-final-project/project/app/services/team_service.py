import logging
import sqlite3
from app.db import get_football_db_conn, get_cursor
from app.helpers.dict import format_dict_nested_keys
from app.constants.clubs import COLORS_KEYS, DETAILS_KEYS


def create_team(team):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.execute('INSERT INTO "teams" ("club_id", "number") VALUES (?, ?)',
                       (team["club_id"], team["number"]))
        conn.commit()
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def get_team(team_id, options):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.row_factory = sqlite3.Row
        colors = options["colors"]
        details = options["details"]
        if colors and details:
            res = cursor.execute('''
                                 SELECT "teams"."id", "number", "teams"."club_id", "clubs"."name" AS "club_name", "club_colors".*, "club_details".*
                                 FROM "teams"
                                 JOIN "clubs" ON "clubs"."id" = "teams"."club_id"
                                 JOIN "club_colors" ON "club_colors"."club_id" = "teams"."club_id"
                                 JOIN "club_details" ON "club_details"."club_id" = "teams"."club_id"
                                 WHERE "teams"."id" = ?''', (team_id,))
        elif colors:
            res = cursor.execute('''
                                 SELECT "teams"."id", "number", "teams"."club_id", "clubs"."name" AS "club_name", "club_colors".*
                                 FROM "teams"
                                 JOIN "clubs" ON "clubs"."id" = "teams"."club_id"
                                 JOIN "club_colors" ON "club_colors"."club_id" = "teams"."club_id"
                                 WHERE "teams"."id" = ?''', (team_id,))
        elif details:
            res = cursor.execute('''
                                 SELECT "teams"."id", "number", "teams"."club_id", "clubs"."name" AS "club_name", "club_details".*
                                 FROM "teams"
                                 JOIN "clubs" ON "clubs"."id" = "teams"."club_id"
                                 JOIN "club_details" ON "club_details"."club_id" = "teams"."club_id"
                                 WHERE "teams"."id" = ?''', (team_id,))
        else:
            res = cursor.execute('''
                                 SELECT "teams"."id", "teams"."number", "teams"."club_id", "clubs"."name" AS "club_name"
                                 FROM "teams" 
                                 JOIN "clubs" ON "clubs"."id" = "teams"."club_id"
                                 WHERE "teams"."id" = ?''', (team_id,))
        try:
            data = dict(res.fetchone())
        except TypeError:
            return None
        data["club"] = {}
        for key in ["name", "id"]:
            data["club"][key] = data[f"club_{key}"]
            del data[f"club_{key}"]
        if colors:
            data = format_dict_nested_keys(data, COLORS_KEYS, ["club", "colors"])
        if details:
            data["club"]["founded"] = data["founded"]
            del data["founded"]
            data = format_dict_nested_keys(data, DETAILS_KEYS, ["club", "address"])
        return data  
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def update_team(team_id, team):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.execute('UPDATE "teams" SET "club_id" = ? AND "number" = ?  WHERE "id" = ?',
                       (team["club_id"], team["number"], team_id))
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def delete_team(team_id):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.execute('DELETE FROM "teams" WHERE "id" = ?', (team_id,))
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def create_team_member(team_id, player_id, seasons):
    try:
        values = [(team_id, player_id, season) for season in seasons]
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.executemany('''
                       INSERT INTO "team_members" ("team_id", "player_id", "season")
                       VALUES (?, ?, ?)''',
                       values)
        conn.commit()
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def get_team_members(team_id, seasons):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        cursor.row_factory = sqlite3.Row
        res_team = cursor.execute('''
                                  SELECT "clubs"."name", "teams"."number"
                                  FROM "teams"
                                  JOIN "clubs" on "clubs"."id" = "teams"."club_id"
                                  WHERE "teams"."id" = ?
                                  ''', (team_id,)).fetchone()
        if len(seasons) == 1:
            res_team_members = cursor.execute('''
                                              SELECT "team_members"."season", "players".*
                                              FROM "team_members"
                                              JOIN "players" ON "players"."id" = "team_members"."player_id"
                                              WHERE "team_members"."team_id" = ?
                                              AND "team_members"."season" = ?
                                              ''', (team_id, seasons[0])).fetchall()
        else: 
            res_team_members = cursor.execute('''
                                              SELECT "team_members"."season", "players".*
                                              FROM "team_members"
                                              JOIN "players" ON "players"."id" = "team_members"."player_id"
                                              WHERE "team_members"."team_id" = ?
                                              AND "team_members"."season" >= ?
                                              AND "team_members"."season" <= ?
                                              ''', (team_id, seasons[0], seasons[-1])).fetchall()
        try:
            data = dict(res_team)
        except TypeError:
            return None
        if len(res_team_members):
            data["team_members"] = {}
            for season in seasons:
                for row in res_team_members:
                    player_data = dict(row)
                    if player_data["season"] == season:
                        del player_data["season"]
                        if not season in data["team_members"]:
                            data["team_members"][season] = []
                        data["team_members"][season].append(player_data)
        else:
            data["team_members"] = None
        return data
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()


def delete_team_member(team_id, player_id, seasons):
    try:
        conn = get_football_db_conn()
        cursor = get_cursor(conn)
        values = [(team_id, player_id, season) for season in seasons]
        cursor.executemany('''
                    DELETE FROM "team_members"
                    WHERE "team_id" = ?
                    AND "player_id" = ? 
                    AND "season" = ?''', 
                    (values))
        conn.commit()
        return True if cursor.rowcount else False
    except sqlite3.Error as err:
        logging.error(err)
        raise
    finally:
        cursor.close()
        conn.close()