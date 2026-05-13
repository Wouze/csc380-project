import sys
import os
from pathlib import Path
import mysql.connector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hotel_app.db import get_connection

def main():
    print("Creating schema...")
    conn = get_connection(with_db=False)
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS hotelmanagement")
    conn.commit()
    conn.close()

    conn = get_connection()
    cursor = conn.cursor()
    
    schema_path = Path(__file__).resolve().parent / "hotel_app" / "schema.sql"
    import re
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Strip comments to prevent syntax errors on execution
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
    print("Done. Run: python -m hotel_app.main")

if __name__ == "__main__":
    main()

