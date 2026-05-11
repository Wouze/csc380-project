"""
Create the configured database and apply schema.sql.

Used by the GUI on first run (unknown DB or missing tables) and by create_schema.py (always full apply).
"""

from __future__ import annotations

import re
from pathlib import Path

from mysql.connector import Error as MySQLError
from mysql.connector import MySQLConnection
from mysql.connector import errorcode

from hotel_app.config import settings
from hotel_app.db import connect

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def _strip_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    out_lines = []
    for line in sql.splitlines():
        if "--" in line:
            line = line[: line.index("--")]
        out_lines.append(line)
    return "\n".join(out_lines)


def _split_statements(sql: str) -> list[str]:
    parts: list[str] = []
    for chunk in _strip_comments(sql).split(";"):
        stmt = chunk.strip()
        if stmt:
            parts.append(stmt)
    return parts


def create_database_if_missing() -> None:
    """Connect without a database catalog and CREATE DATABASE IF NOT EXISTS."""
    cnx = connect(database=None)
    try:
        cur = cnx.cursor()
        db = settings.database
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db}` "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cnx.commit()
        cur.close()
    finally:
        cnx.close()


def apply_schema(cnx: MySQLConnection) -> None:
    """Run every statement in schema.sql (includes DROPs). Caller must use the target database."""
    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(f"Missing schema file: {SCHEMA_PATH}")
    sql_text = SCHEMA_PATH.read_text(encoding="utf-8")
    cur = cnx.cursor()
    try:
        for stmt in _split_statements(sql_text):
            cur.execute(stmt)
        cnx.commit()
    finally:
        cur.close()


def has_hotel_table(cnx: MySQLConnection) -> bool:
    cur = cnx.cursor()
    try:
        cur.execute("SHOW TABLES LIKE 'hotel'")
        return cur.fetchone() is not None
    finally:
        cur.close()


def ensure_ready_for_app() -> bool:
    """
    Ensure the app can open a connection with tables present.

    - If error 1049 (unknown database): create DB, then apply schema if needed.
    - If DB exists but `hotel` table is missing: apply schema.

    Returns True if database or schema was created/applied (first-time setup).
    """
    did_something = False
    try:
        cnx = connect(database=settings.database)
    except MySQLError as e:
        if e.errno != getattr(errorcode, "ER_BAD_DB_ERROR", 1049):
            raise
        create_database_if_missing()
        did_something = True
        cnx = connect(database=settings.database)

    try:
        if not has_hotel_table(cnx):
            apply_schema(cnx)
            did_something = True
    finally:
        cnx.close()

    return did_something


def apply_full_schema_cli() -> None:
    """Always (re)apply schema — used by create_schema.py; resets tables per schema.sql."""
    create_database_if_missing()
    cnx = connect(database=settings.database)
    try:
        apply_schema(cnx)
    finally:
        cnx.close()
