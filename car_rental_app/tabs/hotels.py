import tkinter as tk
from tkinter import messagebox, ttk

from car_rental_app.db import get_connection
from car_rental_app.tabs.common import FIELD_PADY, SEARCH_PADY, create_tree_panel, fill_tree, show_db_error


def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(8, weight=1)

    ttk.Label(frame, text="Branches", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Branch ID").grid(row=1, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w", pady=FIELD_PADY)

    name_var = tk.StringVar()
    ttk.Label(frame, text="Branch Name *").grid(row=2, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=name_var, width=32).grid(row=2, column=1, sticky="w", pady=FIELD_PADY)

    addr_var = tk.StringVar()
    ttk.Label(frame, text="Address *").grid(row=3, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=addr_var, width=32).grid(row=3, column=1, sticky="w", pady=FIELD_PADY)

    city_var = tk.StringVar()
    ttk.Label(frame, text="City *").grid(row=4, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=city_var, width=32).grid(row=4, column=1, sticky="w", pady=FIELD_PADY)

    phone_var = tk.StringVar()
    ttk.Label(frame, text="Phone *").grid(row=5, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=phone_var, width=32).grid(row=5, column=1, sticky="w", pady=FIELD_PADY)

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Name/ID)").grid(row=6, column=0, sticky="w", pady=SEARCH_PADY)
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=6, column=1, sticky="w", pady=SEARCH_PADY)

    cols = ("branch_id", "name", "address", "city", "phone")
    headings = ("Branch ID", "Branch Name", "Address", "City", "Phone")
    tree = create_tree_panel(frame, 8, cols, headings, (80, 150, 200, 100, 100))

    def load_row(_e=None):
        sel = tree.selection()
        if not sel:
            return
        v = tree.item(sel[0], "values")
        id_var.set(str(v[0]))
        name_var.set(v[1])
        addr_var.set(v[2])
        city_var.set(v[3])
        phone_var.set(v[4])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        name_var.set("")
        addr_var.set("")
        city_var.set("")
        phone_var.set("")
        search_var.set("")

    def refresh(search=""):
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search:
                if search.isdigit():
                    cur.execute(
                        "SELECT branch_id, name, address, city, phone FROM branch WHERE branch_id = %s",
                        (int(search),),
                    )
                else:
                    cur.execute(
                        "SELECT branch_id, name, address, city, phone FROM branch WHERE name LIKE %s OR city LIKE %s",
                        ("%" + search + "%", "%" + search + "%"),
                    )
            else:
                cur.execute("SELECT branch_id, name, address, city, phone FROM branch ORDER BY branch_id")
            rows = cur.fetchall()
            cn.close()
            fill_tree(tree, rows)
        except Exception as exc:
            show_db_error(frame, exc)

    def do_search():
        refresh(search_var.get().strip())

    def do_insert():
        if not id_var.get().strip() or not name_var.get().strip() or not addr_var.get().strip() or not city_var.get().strip() or not phone_var.get().strip():
            messagebox.showwarning("Branches", "All * fields required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO branch (branch_id, name, address, city, phone) VALUES (%s,%s,%s,%s,%s)",
                (
                    int(id_var.get()),
                    name_var.get().strip(),
                    addr_var.get().strip(),
                    city_var.get().strip(),
                    phone_var.get().strip(),
                ),
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Branches", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Branches", "Select a record.", parent=frame)
            return
        if not name_var.get().strip() or not addr_var.get().strip() or not city_var.get().strip() or not phone_var.get().strip():
            messagebox.showwarning("Branches", "All * fields required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE branch SET name=%s, address=%s, city=%s, phone=%s WHERE branch_id=%s",
                (
                    name_var.get().strip(),
                    addr_var.get().strip(),
                    city_var.get().strip(),
                    phone_var.get().strip(),
                    int(id_var.get()),
                ),
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Branches", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Branches", "Select a record.", parent=frame)
            return
        if not messagebox.askyesno("Branches", "Delete this branch?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM branch WHERE branch_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Branches", "Deleted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=9, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind("<Visibility>", lambda e: refresh())
    return frame
