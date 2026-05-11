#!/usr/bin/env python3
"""
(Re)create the database and apply hotel_app/schema.sql (drops tables per script).

Uses the same env vars as the GUI (XAMPP defaults: 127.0.0.1:3306, root, hotel_management).

Run from python-hotel-project/:
  python create_schema.py

The GUI also auto-creates an empty DB and tables on first launch; use this script when you
want a clean reset.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

try:
    import mysql.connector  # noqa: F401
except ModuleNotFoundError:
    print("Install dependencies first: python -m pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(1) from None

from hotel_app.config import settings  # noqa: E402
from hotel_app.schema_setup import apply_full_schema_cli  # noqa: E402


def main() -> int:
    print(f"Connecting as {settings.user!r} @ {settings.host}:{settings.port} (database {settings.database!r}) …")
    try:
        apply_full_schema_cli()
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1
    print("Done. Run: python -m hotel_app.main")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
