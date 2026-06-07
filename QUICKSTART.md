# Quick start

## 1. Start MySQL

XAMPP: open Control Panel → **Start** next to MySQL.

## 2. Install Python packages

Open a terminal in **this folder** (`python-hotel-project`):

```bash
python -m pip install -r requirements.txt
```

Use `python -m pip` so it matches the same `python` you run below.

## 3. Run the app

```bash
python -m car_rental_app.main
```

First time: it creates the database `hotel_management` and tables if they are missing (XAMPP defaults: `127.0.0.1`, port `3306`, user `root`, empty password).

## Optional: reset the database

Wipes and rebuilds all tables:

```bash
python create_schema.py
```

## If it fails

- MySQL not running → start it in XAMPP.
- Wrong password → set `HOTEL_DB_PASSWORD` before running, or fix the user in XAMPP.
- `No module named mysql` → run step 2 again with the **same** `python` you use in step 3.

More detail: [README.md](README.md).
