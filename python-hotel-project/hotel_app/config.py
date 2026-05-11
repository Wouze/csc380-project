import os
from typing import Optional


def getenv(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.environ.get(name)
    if v is None or v.strip() == "":
        return default
    return v.strip()


# Defaults match a typical XAMPP / local MariaDB install (no env vars required).
class DatabaseSettings:
    host: str = getenv("HOTEL_DB_HOST") or "127.0.0.1"
    port: int = int(getenv("HOTEL_DB_PORT") or "3306")
    database: str = getenv("HOTEL_DB_NAME") or "hotel_management"
    user: str = getenv("HOTEL_DB_USER") or "root"
    password: Optional[str] = getenv("HOTEL_DB_PASSWORD")
    # Set for XAMPP/WAMP installs that expose MySQL only via Unix socket (see README).
    unix_socket: Optional[str] = getenv("HOTEL_DB_UNIX_SOCKET")


settings = DatabaseSettings()
