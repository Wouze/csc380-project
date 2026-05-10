from contextlib import contextmanager
from typing import Generator

import mysql.connector
from mysql.connector import MySQLConnection

from hotel_app.config import settings


@contextmanager
def get_connection() -> Generator[MySQLConnection, None, None]:
    common = {
        "user": settings.user,
        "password": settings.password or "",
        "database": settings.database,
    }
    if settings.unix_socket:
        conn = mysql.connector.connect(unix_socket=settings.unix_socket, **common)
    else:
        conn = mysql.connector.connect(
            host=settings.host,
            port=settings.port,
            **common,
        )
    try:
        yield conn
    finally:
        conn.close()
