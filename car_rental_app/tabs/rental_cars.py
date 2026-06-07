import tkinter as tk
from tkinter import ttk

from car_rental_app.db import get_connection
from car_rental_app.tabs.common import (
    FIELD_PADY,
    SEARCH_PADY,
    ask_yes_no,
    create_tree_panel,
    show_db_error,
    show_info,
    show_warning,
)


def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(6, weight=1)

    ttk.Label(frame, text="Rental Cars", font=("", 14, "bold")).grid(
        row=0, column=0, columnspan=3, sticky="w", pady=(0, 8)
    )

    rental_var = tk.StringVar()
    ttk.Label(frame, text="Rental ID *").grid(row=1, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=rental_var, width=12).grid(row=1, column=1, sticky="w", pady=FIELD_PADY)

    car_var = tk.StringVar()
    ttk.Label(frame, text="Car ID *").grid(row=2, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=car_var, width=12).grid(row=2, column=1, sticky="w", pady=FIELD_PADY)

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Rental ID)").grid(row=3, column=0, sticky="w", pady=SEARCH_PADY)
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=3, column=1, sticky="w", pady=SEARCH_PADY)

    cols = ("rental_id", "car_id")
    headings = ("Rental ID", "Car ID")
    tree = create_tree_panel(frame, 6, cols, headings, (100, 100))

    selected = {"rental_id": None, "car_id": None}

    def load_row(_e=None):
        sel = tree.selection()
        if not sel:
            return
        v = tree.item(sel[0], "values")
        selected["rental_id"] = int(v[0])
        selected["car_id"] = int(v[1])
        rental_var.set(str(v[0]))
        car_var.set(str(v[1]))

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        rental_var.set("")
        car_var.set("")
        search_var.set("")
        selected["rental_id"] = None
        selected["car_id"] = None

    def refresh(search=""):
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search and search.isdigit():
                cur.execute(
                    "SELECT rental_id, car_id FROM rental_car WHERE rental_id = %s ORDER BY rental_id, car_id",
                    (int(search),),
                )
            else:
                cur.execute("SELECT rental_id, car_id FROM rental_car ORDER BY rental_id, car_id")
            rows = cur.fetchall()
            cn.close()
            tree.delete(*tree.get_children())
            for row in rows:
                tree.insert("", tk.END, iid=f"{row[0]}_{row[1]}", values=(str(row[0]), str(row[1])))
        except Exception as exc:
            show_db_error(frame, exc)

    def do_search():
        refresh(search_var.get().strip())

    def do_insert():
        if not rental_var.get().strip() or not car_var.get().strip():
            show_warning(frame, "Rental Cars", "Required fields missing.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO rental_car (rental_id, car_id) VALUES (%s, %s)",
                (int(rental_var.get()), int(car_var.get())),
            )
            cn.commit()
            cn.close()
            show_info(frame, "Rental Cars", "Inserted successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if selected["rental_id"] is None or selected["car_id"] is None:
            show_warning(frame, "Rental Cars", "Select a record.")
            return
        if not rental_var.get().strip() or not car_var.get().strip():
            show_warning(frame, "Rental Cars", "Required fields missing.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "DELETE FROM rental_car WHERE rental_id = %s AND car_id = %s",
                (selected["rental_id"], selected["car_id"]),
            )
            cur.execute(
                "INSERT INTO rental_car (rental_id, car_id) VALUES (%s, %s)",
                (int(rental_var.get()), int(car_var.get())),
            )
            cn.commit()
            cn.close()
            show_info(frame, "Rental Cars", "Updated successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if selected["rental_id"] is None or selected["car_id"] is None:
            show_warning(frame, "Rental Cars", "Select a record.")
            return
        if not ask_yes_no(frame, "Rental Cars", "Delete this rental-car link?"):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "DELETE FROM rental_car WHERE rental_id = %s AND car_id = %s",
                (selected["rental_id"], selected["car_id"]),
            )
            cn.commit()
            cn.close()
            show_info(frame, "Rental Cars", "Deleted successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=7, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind("<Visibility>", lambda e: refresh())
    return frame
