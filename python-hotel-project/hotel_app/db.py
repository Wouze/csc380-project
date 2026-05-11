from contextlib import contextmanager
from typing import Generator, Optional

import mysql.connector
from mysql.connector import MySQLConnection

from hotel_app.config import settings


def connect(database: Optional[str] = None) -> MySQLConnection:
    """Open one connection. ``database=None`` connects without selecting a catalog (for CREATE DATABASE)."""
    common: dict = {
        "user": settings.user,
        "password": settings.password or "",
    }
    if database is not None:
        common["database"] = database
    if settings.unix_socket:
        return mysql.connector.connect(unix_socket=settings.unix_socket, **common)
    return mysql.connector.connect(host=settings.host, port=settings.port, **common)


@contextmanager
def get_connection() -> Generator[MySQLConnection, None, None]:
    conn = connect(database=settings.database)
    try:
        yield conn
    finally:
        conn.close()
