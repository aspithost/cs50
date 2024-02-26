import sqlite3
from app.constants.db import FOOTBALL_DB, SCHEMA_PATH


def get_conn(db):
    with sqlite3.connect(db) as conn:
        return conn


def get_cursor(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return cursor


def get_football_db_conn():
    return get_conn(FOOTBALL_DB)


def init_football_db():
    conn = get_football_db_conn()
    cursor = get_cursor(conn)
    try:
        with open(SCHEMA_PATH, "r") as sql_schema:
            sql_script = sql_schema.read()
            try:
                cursor.executescript(sql_script)
                print("database initialized successfully!")
            except sqlite3.Error as err:
                print(f"Error initializing database: {str(err)}")
    except FileNotFoundError as err:
        print(f"File not found: {str(err)}")
    finally:
        cursor.close()