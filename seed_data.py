"""Load sample demo data into the car_rental database."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from car_rental_app.db import get_connection


def clear_tables(cursor):
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in ("invoice", "payment", "rental_car", "rental", "car", "customer", "branch"):
        cursor.execute(f"DELETE FROM {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


def seed(cursor):
    cursor.executemany(
        "INSERT INTO branch (branch_id, name, address, city, phone) VALUES (%s,%s,%s,%s,%s)",
        [
            (1, "Al Olaya Branch", "Al Olaya", "Riyadh", "0561112233"),
            (2, "Corniche Rentals", "Al Hamra", "Jeddah", "0562223344"),
            (3, "Dammam Airport", "Al Faisaliyah", "Dammam", "0563334455"),
        ],
    )

    cursor.executemany(
        "INSERT INTO customer (customer_id, first_name, last_name, email, phone, nationality) VALUES (%s,%s,%s,%s,%s,%s)",
        [
            (1, "fahad", "alqahtani", "fahad.qht@hotmail.com", "0565123456", "Saudi"),
            (2, "noura", "alharbi", "noura_1992@hotmail.com", "0564221889", "Saudi Arabian"),
            (3, "mohammed", "alsaud", "mohammed.alsaud@hotmail.com", "0567788990", "Saudi"),
            (4, "ahmed", "khan", "ahmedkhan88@hotmail.com", "0563441220", "Pakistani"),
            (5, "layla", "hassan", "layla.h@hotmail.com", "0565011223", "Egyptian"),
            (6, "omar", "alghamdi", "omar.g@hotmail.com", "0569981122", ""),
        ],
    )

    cursor.executemany(
        "INSERT INTO car (car_id, license_plate, model_year, car_type, daily_rate, seats, status, branch_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        [
            (1, "BTR 8891", 2022, "Economy", 180.00, 5, "Available", 1),
            (2, "HGR 4521", 2023, "SUV", 320.00, 7, "Available", 1),
            (3, "RHM 2045", 2021, "Compact", 150.00, 4, "Rented", 2),
            (4, "ABC 5512", 2024, "Luxury", 550.00, 5, "Available", 2),
            (5, "KHR 3310", 2020, "Economy", 165.50, 5, "Maintenance", 1),
            (6, "DTB 7788", 2023, "SUV", 285.00, 7, "Available", 3),
            (7, "SDR 1199", 2022, "Compact", 175.00, 4, "Rented", 3),
        ],
    )

    cursor.executemany(
        "INSERT INTO rental (rental_id, booking_date, pick_up_date, return_date, status, customer_id) VALUES (%s,%s,%s,%s,%s,%s)",
        [
            (1, "2026-05-28", "2026-06-02", "2026-06-07", "confirmed", 1),
            (2, "2026-06-01", "2026-06-05", "2026-06-09", "active", 2),
            (3, "2026-05-15", "2026-05-20", "2026-05-24", "returned", 3),
            (4, "2026-06-04", "2026-06-10", "2026-06-14", "confirmed", 4),
            (5, "2026-05-10", "2026-05-12", "2026-05-15", "returned", 5),
            (6, "2026-06-06", "2026-06-08", "2026-06-11", "active", 6),
        ],
    )

    cursor.executemany(
        "INSERT INTO rental_car (rental_id, car_id) VALUES (%s,%s)",
        [
            (1, 1),
            (2, 3),
            (3, 2),
            (4, 4),
            (5, 6),
            (6, 7),
        ],
    )

    cursor.executemany(
        "INSERT INTO payment (payment_id, rental_id, total_amount, payment_method, payment_status, issue_date) VALUES (%s,%s,%s,%s,%s,%s)",
        [
            (1, 1, 900.00, "mada", "pending", "2026-05-28"),
            (2, 2, 600.00, "Credit Card", "paid", "2026-06-01"),
            (3, 3, 1280.00, "cash", "paid", "2026-05-15"),
            (4, 5, 855.00, "Mada", "paid", "2026-05-10"),
            (5, 6, 525.50, "credit card", "pending", "2026-06-06"),
        ],
    )

    cursor.executemany(
        "INSERT INTO invoice (invoice_id, payment_id, invoice_number) VALUES (%s,%s,%s)",
        [
            (1, 2, "INV-2026-001"),
            (2, 3, "INV-2026-002"),
            (3, 4, "INV-2026-003"),
        ],
    )


def main():
    print("Seeding car_rental with sample data...")
    conn = get_connection()
    cursor = conn.cursor()

    try:
        clear_tables(cursor)
        seed(cursor)
        conn.commit()
    except Exception as exc:
        conn.rollback()
        print(f"Failed: {exc}")
        print("Make sure MySQL is running and you ran: python create_schema.py")
        raise SystemExit(1) from exc
    finally:
        cursor.close()
        conn.close()

    print("Done.")
    print("  3 branches, 6 customers, 7 cars")
    print("  6 rentals (with rental_car links), 5 payments, 3 invoices")
    print("Run: python -m car_rental_app.main")


if __name__ == "__main__":
    main()
