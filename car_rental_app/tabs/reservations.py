import tkinter as tk
from tkinter import ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import (
    FIELD_PADY,
    SEARCH_PADY,
    ask_yes_no,
    create_tree_panel,
    fill_tree,
    set_combo_by_label,
    show_db_error,
    show_info,
    show_warning,
)

_RENTAL_SELECT = """
    SELECT r.rental_id,
           CONCAT(cu.first_name, ' ', cu.last_name),
           COALESCE(GROUP_CONCAT(DISTINCT car.license_plate ORDER BY car.car_id SEPARATOR ', '), ''),
           r.booking_date, r.pick_up_date, r.return_date, r.status
    FROM rental r
    LEFT JOIN customer cu ON r.customer_id = cu.customer_id
    LEFT JOIN rental_car rc ON r.rental_id = rc.rental_id
    LEFT JOIN car ON rc.car_id = car.car_id
"""


def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(10, weight=1)

    ttk.Label(frame, text="Rentals", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Rental ID").grid(row=1, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w", pady=FIELD_PADY)

    guest_var = tk.StringVar()
    ttk.Label(frame, text="Customer *").grid(row=2, column=0, sticky="w", pady=FIELD_PADY)
    guest_combo = ttk.Combobox(frame, textvariable=guest_var, width=36, state="readonly")
    guest_combo.grid(row=2, column=1, sticky="w", pady=FIELD_PADY)

    car_var = tk.StringVar()
    ttk.Label(frame, text="Car *").grid(row=3, column=0, sticky="w", pady=FIELD_PADY)
    car_combo = ttk.Combobox(frame, textvariable=car_var, width=36, state="readonly")
    car_combo.grid(row=3, column=1, sticky="w", pady=FIELD_PADY)

    booking_var = tk.StringVar()
    ttk.Label(frame, text="Booking Date *").grid(row=4, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=booking_var, width=16).grid(row=4, column=1, sticky="w", pady=FIELD_PADY)
    ttk.Label(frame, text="(YYYY-MM-DD)", foreground="gray").grid(row=4, column=2, sticky="w", pady=FIELD_PADY)

    in_var = tk.StringVar()
    ttk.Label(frame, text="Pick-up Date *").grid(row=5, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=in_var, width=16).grid(row=5, column=1, sticky="w", pady=FIELD_PADY)
    ttk.Label(frame, text="(YYYY-MM-DD)", foreground="gray").grid(row=5, column=2, sticky="w", pady=FIELD_PADY)

    out_var = tk.StringVar()
    ttk.Label(frame, text="Return Date *").grid(row=6, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=out_var, width=16).grid(row=6, column=1, sticky="w", pady=FIELD_PADY)
    ttk.Label(frame, text="(YYYY-MM-DD)", foreground="gray").grid(row=6, column=2, sticky="w", pady=FIELD_PADY)

    status_var = tk.StringVar()
    ttk.Label(frame, text="Status *").grid(row=7, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Combobox(frame, textvariable=status_var, values=("confirmed", "active", "returned", "cancelled"), width=16, state="readonly").grid(row=7, column=1, sticky="w", pady=FIELD_PADY)

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Rental ID)").grid(row=8, column=0, sticky="w", pady=SEARCH_PADY)
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=8, column=1, sticky="w", pady=SEARCH_PADY)

    cols = ("rental_id", "customer", "cars", "booking_date", "pick_up_date", "return_date", "status")
    headings = ("Rental ID", "Customer", "Car(s)", "Booking Date", "Pick-up Date", "Return Date", "Status")
    tree = create_tree_panel(frame, 10, cols, headings, (70, 120, 100, 90, 90, 90, 80))

    def load_combos():
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("SELECT customer_id, first_name, last_name FROM customer ORDER BY customer_id")
            guest_combo["values"] = [f"{r[0]} | {r[1]} {r[2]}" for r in cur.fetchall()]
            cur.execute(
                "SELECT car_id, license_plate, car_type FROM car ORDER BY car_id"
            )
            car_combo["values"] = [
                f"{r[0]} | {r[1]} ({r[2]})" if r[1] else f"{r[0]} | Car {r[0]} ({r[2]})"
                for r in cur.fetchall()
            ]
            cn.close()
        except Exception:
            pass

    def get_combo_id(val):
        if not val.strip():
            return None
        return int(val.split("|")[0].strip())

    def set_car_combo_for_rental(rental_id):
        car_var.set("")
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "SELECT car_id FROM rental_car WHERE rental_id = %s ORDER BY car_id LIMIT 1",
                (int(rental_id),),
            )
            row = cur.fetchone()
            cn.close()
            if row:
                car_id = str(row[0])
                for val in car_combo["values"]:
                    if val.startswith(car_id + " |"):
                        car_combo.set(val)
                        break
        except Exception:
            pass

    def load_row(_e=None):
        sel = tree.selection()
        if not sel:
            return
        v = tree.item(sel[0], "values")
        id_var.set(str(v[0]))
        set_combo_by_label(guest_combo, v[1])
        set_car_combo_for_rental(v[0])
        booking_var.set(v[3])
        in_var.set(v[4])
        out_var.set(v[5])
        status_var.set(v[6])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        guest_var.set("")
        car_var.set("")
        booking_var.set("")
        in_var.set("")
        out_var.set("")
        status_var.set("")
        search_var.set("")

    def _group_clause(where_sql=""):
        return (
            _RENTAL_SELECT
            + where_sql
            + """
    GROUP BY r.rental_id, cu.first_name, cu.last_name,
             r.booking_date, r.pick_up_date, r.return_date, r.status
    """
        )

    def refresh(search=""):
        load_combos()
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search:
                if search.isdigit():
                    cur.execute(
                        _group_clause("WHERE r.rental_id = %s") + "ORDER BY r.rental_id",
                        (int(search),),
                    )
                else:
                    cur.execute(
                        _group_clause("WHERE r.status LIKE %s") + "ORDER BY r.rental_id",
                        ("%" + search + "%",),
                    )
            else:
                cur.execute(_group_clause() + "ORDER BY r.rental_id")
            rows = cur.fetchall()
            cn.close()
            fill_tree(tree, rows)
        except Exception as exc:
            show_db_error(frame, exc)

    def link_car(cur, rental_id, car_id):
        cur.execute("DELETE FROM rental_car WHERE rental_id = %s", (rental_id,))
        cur.execute(
            "INSERT INTO rental_car (rental_id, car_id) VALUES (%s, %s)",
            (rental_id, car_id),
        )

    def do_search():
        refresh(search_var.get().strip())

    def do_insert():
        gid = get_combo_id(guest_var.get())
        cid = get_combo_id(car_var.get())
        if (
            not id_var.get().strip()
            or not gid
            or not cid
            or not booking_var.get().strip()
            or not in_var.get().strip()
            or not out_var.get().strip()
            or not status_var.get().strip()
        ):
            show_warning(frame, "Rentals", "Required fields missing.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            rental_id = int(id_var.get())
            cur.execute(
                "INSERT INTO rental (rental_id, customer_id, booking_date, pick_up_date, return_date, status) VALUES (%s,%s,%s,%s,%s,%s)",
                (
                    rental_id,
                    gid,
                    booking_var.get().strip(),
                    in_var.get().strip(),
                    out_var.get().strip(),
                    status_var.get(),
                ),
            )
            link_car(cur, rental_id, cid)
            cn.commit()
            cn.close()
            show_info(frame, "Rentals", "Inserted successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            show_warning(frame, "Rentals", "Select a record.")
            return
        gid = get_combo_id(guest_var.get())
        cid = get_combo_id(car_var.get())
        if (
            not gid
            or not cid
            or not booking_var.get().strip()
            or not in_var.get().strip()
            or not out_var.get().strip()
            or not status_var.get().strip()
        ):
            show_warning(frame, "Rentals", "Required fields missing.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            rental_id = int(id_var.get())
            cur.execute(
                "UPDATE rental SET customer_id=%s, booking_date=%s, pick_up_date=%s, return_date=%s, status=%s WHERE rental_id=%s",
                (
                    gid,
                    booking_var.get().strip(),
                    in_var.get().strip(),
                    out_var.get().strip(),
                    status_var.get(),
                    rental_id,
                ),
            )
            link_car(cur, rental_id, cid)
            cn.commit()
            cn.close()
            show_info(frame, "Rentals", "Updated successfully.")
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            show_warning(frame, "Rentals", "Select a record.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            rental_id = int(id_var.get())
            cur.execute("SELECT COUNT(*) FROM rental_car WHERE rental_id = %s", (rental_id,))
            car_links = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM payment WHERE rental_id = %s", (rental_id,))
            payments = cur.fetchone()[0]
            cn.close()

            msg = f"Delete rental {rental_id}?"
            if car_links or payments:
                msg += (
                    f"\n\nThis will also remove {car_links} car link(s)"
                    f" and {payments} payment(s)."
                )
            if not ask_yes_no(frame, "Rentals", msg):
                return

            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM rental WHERE rental_id = %s", (rental_id,))
            cn.commit()
            cn.close()
            show_info(frame, "Rentals", "Deleted successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=11, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind("<Visibility>", lambda e: refresh())
    return frame
