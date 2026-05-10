# Hotel Management System (Python + Tkinter + MySQL)

Desktop CRUD client for the hotel schema used in **CSC 380** (hotels, rooms, guests, reservations, reservation–room lines, invoices, employees).  
The UI is **Tkinter** with one tab per entity; SQL is sent to **MySQL** via `mysql-connector-python` (parameterized queries).

The older **Java Swing** library system lives in the sibling folder **`java-library-project/`** in this repository.

## Requirements

- **Python 3.10+** (uses `list[str]` / `|` type syntax; use 3.9+ with small edits if needed)
- **MySQL or MariaDB** — the stack included with **XAMPP** is fine
- Network access to the DB (default: `127.0.0.1:3306`)

## Connect using XAMPP

XAMPP ships **MariaDB** (MySQL-compatible) and starts it from the **XAMPP Control Panel**.

1. **Start MySQL** (Apache is not required for this app).
2. Confirm the port is **3306** (XAMPP default). If another program uses 3306, change the port in XAMPP’s `my.ini` / `my.cnf` and set `HOTEL_DB_PORT` to match.
3. **Create the database** and load the schema:
   - **Option A — phpMyAdmin** (often `http://localhost/phpmyadmin`):
     - New database: `hotel_management`
     - Import tab → choose `hotel_app/schema.sql` → Go.
   - **Option B — command line** (paths vary by OS):

     ```bash
     # Example: XAMPP’s mysql client on Windows (adjust path)
     # "C:\xampp\mysql\bin\mysql.exe" -u root -p -e "CREATE DATABASE IF NOT EXISTS hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
     # "C:\xampp\mysql\bin\mysql.exe" -u root -p hotel_management < hotel_app/schema.sql
     ```

     On macOS/Linux with `mysql` on your `PATH`:

     ```bash
     mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hotel_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
     mysql -u root -p hotel_management < hotel_app/schema.sql
     ```

4. **Typical XAMPP credentials**

   | Setting   | Common XAMPP default |
   |----------|-----------------------|
   | Host     | `127.0.0.1`           |
   | Port     | `3306`                |
   | User     | `root`                |
   | Password | *(empty)*             |
   | Database | `hotel_management`    |

   You do **not** need to set any environment variables if these defaults match your install; the app uses them automatically. Set `HOTEL_DB_PASSWORD` only if you assigned a root password in XAMPP.

5. **Optional: Unix socket (some macOS/Linux XAMPP layouts)**  
   If TCP to `127.0.0.1:3306` fails but the server is running, try the socket file XAMPP documents (example path only—check your install):

   ```bash
   export HOTEL_DB_UNIX_SOCKET="/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"
   ```

   When `HOTEL_DB_UNIX_SOCKET` is set, `HOTEL_DB_HOST` / `HOTEL_DB_PORT` are not used for the connection.

## Python setup

From this folder (`python-hotel-project/`):

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOTEL_DB_HOST` | `127.0.0.1` | MySQL/MariaDB host (ignored if `UNIX_SOCKET` is set) |
| `HOTEL_DB_PORT` | `3306` | Port |
| `HOTEL_DB_NAME` | `hotel_management` | Database name |
| `HOTEL_DB_USER` | `root` | Username |
| `HOTEL_DB_PASSWORD` | *(empty)* | Password; omit or leave unset for blank password |
| `HOTEL_DB_UNIX_SOCKET` | *(unset)* | Full path to `mysql.sock` for socket-only installs |

Example with a non-empty password:

```bash
export HOTEL_DB_USER=root
export HOTEL_DB_PASSWORD='your_password'
export HOTEL_DB_NAME=hotel_management
python -m hotel_app.main
```

## Run the application

From this folder (`python-hotel-project/` in the repo root, so `hotel_app` is importable):

```bash
python -m hotel_app.main
```

On startup, the app runs a simple `SELECT 1` against the database; if that fails, check that XAMPP **MySQL is running**, the database exists, and credentials match.

## Project layout

| Path | Purpose |
|------|---------|
| `hotel_app/schema.sql` | Tables, FKs, and constraints |
| `hotel_app/main.py` | Window, tabbed notebook, tab refresh on switch |
| `hotel_app/config.py` | Environment-based DB settings |
| `hotel_app/db.py` | `get_connection()` context manager |
| `hotel_app/tabs/*.py` | One module per CRUD tab |

## Troubleshooting (XAMPP)

- **`Can't connect to MySQL server`** — Start MySQL in XAMPP; confirm port 3306 is not blocked or changed.
- **`Access denied for user 'root'`** — Set `HOTEL_DB_USER` / `HOTEL_DB_PASSWORD` to match what you configured in XAMPP/phpMyAdmin.
- **`Unknown database 'hotel_management'`** — Create the database and run `hotel_app/schema.sql` (see above).
- **Tab refreshes when you switch** — Designed so pick-lists stay in sync after changes in other tabs; use **Refresh** on a tab if data looks stale.

## License / course use

Use and adapt for CSC 380 coursework as needed.
