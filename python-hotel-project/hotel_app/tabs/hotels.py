
import tkinter as tk
from tkinter import messagebox, ttk

from hotel_app.db import get_connection
from hotel_app.tabs.common import clear_tree, show_db_error


def build(parent) :
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(6, weight=1)

    ttk.Label(frame, text="Hotels", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 8))

    ttk.Label(frame, text="Hotel ID (auto on insert)").grid(row=1, column=0, sticky="w", pady=2)
    hotel_id_var = tk.StringVar()
    ttk.Entry(frame, textvariable=hotel_id_var, width=14, state="readonly").grid(row=1, column=1, sticky="w", pady=2)

    ttk.Label(frame, text="Name *").grid(row=2, column=0, sticky="w", pady=2)
    name_var = tk.StringVar()
    ttk.Entry(frame, textvariable=name_var, width=40).grid(row=2, column=1, columnspan=2, sticky="we", pady=2)

    ttk.Label(frame, text="Address *").grid(row=3, column=0, sticky="w", pady=2)
    address_var = tk.StringVar()
    ttk.Entry(frame, textvariable=address_var, width=40).grid(row=3, column=1, columnspan=2, sticky="we", pady=2)

    ttk.Label(frame, text="City *").grid(row=4, column=0, sticky="w", pady=2)
    city_var = tk.StringVar()
    ttk.Entry(frame, textvariable=city_var, width=40).grid(row=4, column=1, columnspan=2, sticky="we", pady=2)

    ttk.Label(frame, text="Phone *").grid(row=5, column=0, sticky="w", pady=2)
    phone_var = tk.StringVar()
    ttk.Entry(frame, textvariable=phone_var, width=40).grid(row=5, column=1, columnspan=2, sticky="we", pady=2)

    cols = ("hotel_id", "name", "address", "city", "phone")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (70, 140, 220, 100, 120)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=6, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_row_to_form(_event=None) :
        sel = tree.selection()
        if not sel:
            return
        vals = tree.item(sel[0], "values")
        hotel_id_var.set(str(vals[0]))
        name_var.set(vals[1])
        address_var.set(vals[2])
        city_var.set(vals[3])
        phone_var.set(vals[4])

    tree.bind("<<TreeviewSelect>>", load_row_to_form)

    def clear_form() :
        hotel_id_var.set("")
        name_var.set("")
        address_var.set("")
        city_var.set("")
        phone_var.set("")

    def refresh() :
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "SELECT hotel_id, name, address, city, phone FROM hotel ORDER BY hotel_id"
            )
            rows = cur.fetchall()
            cn.close()
            clear_tree(tree)
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), values=r)
            clear_form()
        except Exception as exc:
            show_db_error(frame, exc)

    def insert_hotel() :
        try:
            if not name_var.get().strip():
                messagebox.showwarning("Validation", "Name is required.", parent=frame)
                return
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO hotel (name, address, city, phone) VALUES (%s,%s,%s,%s)",
                (
                    name_var.get().strip(),
                    address_var.get().strip(),
                    city_var.get().strip(),
                    phone_var.get().strip(),
                ),
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Hotels", "Hotel inserted.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def update_hotel() :
        try:
            hid = hotel_id_var.get().strip()
            if not hid:
                messagebox.showwarning("Hotels", "Select a hotel to update.", parent=frame)
                return
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE hotel SET name=%s, address=%s, city=%s, phone=%s WHERE hotel_id=%s",
                (
                    name_var.get().strip(),
                    address_var.get().strip(),
                    city_var.get().strip(),
                    phone_var.get().strip(),
                    int(hid),
                ),
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Hotels", "Hotel updated.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def delete_hotel() :
        try:
            hid = hotel_id_var.get().strip()
            if not hid:
                messagebox.showwarning("Hotels", "Select a hotel to delete.", parent=frame)
                return
            if not messagebox.askyesno("Hotels", "Delete this hotel? (Blocked if rooms or employees exist.)", parent=frame):
                return
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM hotel WHERE hotel_id=%s", (int(hid),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Hotels", "Hotel deleted.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btns = ttk.Frame(frame)
    btns.grid(row=7, column=0, columnspan=3, sticky="w")
    ttk.Button(btns, text="Insert", command=insert_hotel).pack(side="left", padx=(0, 6))
    ttk.Button(btns, text="Update", command=update_hotel).pack(side="left", padx=6)
    ttk.Button(btns, text="Delete", command=delete_hotel).pack(side="left", padx=6)
    ttk.Button(btns, text="Refresh", command=refresh).pack(side="left", padx=6)
    ttk.Button(btns, text="Clear form", command=clear_form).pack(side="left", padx=6)

    refresh()
    frame.bind('<Visibility>', lambda e: refresh())
    refresh()
    return frame
