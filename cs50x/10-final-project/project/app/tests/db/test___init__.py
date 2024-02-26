import pytest
import sqlite3
from app.db import (
    get_conn,
    get_cursor,
    get_football_db_conn,
    init_football_db,
)
from app.constants.db import FOOTBALL_DB, SCHEMA_PATH


@pytest.fixture
def temp_db():
    db_path = "test_db.sqlite"
    conn = sqlite3.connect(db_path)
    yield db_path
    conn.close()


def test_get_conn(temp_db):
    db_path = temp_db
    conn = get_conn(db_path)

    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_get_cursor(temp_db):
    db_path = temp_db
    conn = get_conn(db_path)
    
    cursor = get_cursor(conn)

    assert isinstance(cursor, sqlite3.Cursor)

    cursor.execute("PRAGMA foreign_keys;")
    result = cursor.fetchone()
    assert result[0] == 1  # 1 indicates that foreign key support is enabled

    cursor.close()
    conn.close()


def test_get_football_db_conn():
    conn = get_football_db_conn()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_init_football_db(capsys):
    init_football_db()

    captured = capsys.readouterr()

    assert "database initialized successfully!" in captured.out