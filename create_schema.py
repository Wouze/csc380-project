import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from car_rental_app.db import get_connection


def main():
    print("Dropping old hotelmanagement database (if exists)...")
    conn = get_connection(with_db=False)
    cursor = conn.cursor()
    cursor.execute("DROP DATABASE IF EXISTS hotelmanagement")
    cursor.execute("DROP DATABASE IF EXISTS car_rental")
    cursor.execute("CREATE DATABASE car_rental")
    conn.commit()
    conn.close()

    print("Creating car_rental schema...")
    conn = get_connection()
    cursor = conn.cursor()

    schema_path = Path(__file__).resolve().parent / "car_rental_app" / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    out_lines = []
    for line in sql.splitlines():
        if "--" in line:
            line = line[: line.index("--")]
        out_lines.append(line)
    sql = "\n".join(out_lines)

    for statement in sql.split(";"):
        if statement.strip():
            cursor.execute(statement)

    conn.commit()
    conn.close()
    print("Done. Database 'car_rental' is ready.")
    print("Run: python -m car_rental_app.main")


if __name__ == "__main__":
    main()
