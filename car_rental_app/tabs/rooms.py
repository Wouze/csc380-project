import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import FIELD_PADY, SEARCH_PADY, clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(11, weight=1)

    ttk.Label(frame, text="Cars", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Car ID").grid(row=1, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w", pady=FIELD_PADY)

    hotel_var = tk.StringVar()
    ttk.Label(frame, text="Branch *").grid(row=2, column=0, sticky="w", pady=FIELD_PADY)
    hotel_combo = ttk.Combobox(frame, textvariable=hotel_var, width=36, state="readonly")
    hotel_combo.grid(row=2, column=1, sticky="w", pady=FIELD_PADY)

    room_num_var = tk.StringVar()
    ttk.Label(frame, text="License Plate *").grid(row=3, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=room_num_var, width=16).grid(row=3, column=1, sticky="w", pady=FIELD_PADY)

    floor_var = tk.StringVar()
    ttk.Label(frame, text="Model Year *").grid(row=4, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=floor_var, width=16).grid(row=4, column=1, sticky="w", pady=FIELD_PADY)

    type_var = tk.StringVar()
    ttk.Label(frame, text="Car Type *").grid(row=5, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Combobox(frame, textvariable=type_var, values=("Economy", "Compact", "SUV", "Luxury"), width=16, state="readonly").grid(row=5, column=1, sticky="w", pady=FIELD_PADY)

    price_var = tk.StringVar()
    ttk.Label(frame, text="Daily Rate *").grid(row=6, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=price_var, width=16).grid(row=6, column=1, sticky="w", pady=FIELD_PADY)

    cap_var = tk.StringVar()
    ttk.Label(frame, text="Seats *").grid(row=7, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=cap_var, width=16).grid(row=7, column=1, sticky="w", pady=FIELD_PADY)

    status_var = tk.StringVar()
    ttk.Label(frame, text="Status *").grid(row=8, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Combobox(frame, textvariable=status_var, values=("Available", "Rented", "Maintenance"), width=16, state="readonly").grid(row=8, column=1, sticky="w", pady=FIELD_PADY)

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Car ID)").grid(row=9, column=0, sticky="w", pady=SEARCH_PADY)
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=9, column=1, sticky="w", pady=SEARCH_PADY)

    cols = ("car_id", "branch_id", "license_plate", "model_year", "car_type", "daily_rate", "seats", "status")
    headings = ("Car ID", "Branch ID", "License Plate", "Model Year", "Car Type", "Daily Rate", "Seats", "Status")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, h, w in zip(cols, headings, (60, 60, 90, 70, 80, 90, 50, 80)):
        tree.heading(c, text=h)
        tree.column(c, width=w, anchor="w")
    tree.grid(row=11, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=11, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_combos():
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("SELECT branch_id, name FROM branch ORDER BY branch_id")
            rows = cur.fetchall()
            cn.close()
            hotel_combo["values"] = [f"{r[0]} | {r[1]}" for r in rows]
        except Exception:
            pass

    def get_combo_id(val):
        if not val.strip(): return None
        return int(val.split("|")[0].strip())

    def load_row(_e=None):
        sel = tree.selection()
        if not sel: return
        v = tree.item(sel[0], "values")
        id_var.set(str(v[0]))
        hid = str(v[1])
        for val in hotel_combo["values"]:
            if val.startswith(hid + " |"):
                hotel_combo.set(val)
                break
        room_num_var.set(v[2])
        floor_var.set(str(v[3]))
        type_var.set(v[4])
        price_var.set(str(v[5]))
        cap_var.set(str(v[6]))
        status_var.set(v[7])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        hotel_var.set("")
        room_num_var.set("")
        floor_var.set("")
        type_var.set("")
        price_var.set("")
        cap_var.set("")
        status_var.set("")
        search_var.set("")

    def refresh(search=""):
        load_combos()
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search:
                if search.isdigit():
                    cur.execute("SELECT car_id, branch_id, license_plate, model_year, car_type, daily_rate, seats, status FROM car WHERE car_id = %s", (int(search),))
                else:
                    cur.execute("SELECT car_id, branch_id, license_plate, model_year, car_type, daily_rate, seats, status FROM car WHERE license_plate LIKE %s", ("%" + search + "%",))
            else:
                cur.execute("SELECT car_id, branch_id, license_plate, model_year, car_type, daily_rate, seats, status FROM car ORDER BY car_id")
            rows = cur.fetchall()
            cn.close()
            clear_tree(tree)
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), values=r)
        except Exception as exc:
            show_db_error(frame, exc)

    def do_search():
        refresh(search_var.get().strip())

    def do_insert():
        hid = get_combo_id(hotel_var.get())
        if not id_var.get().strip() or not hid or not room_num_var.get().strip() or not floor_var.get().strip() or not type_var.get().strip() or not price_var.get().strip() or not cap_var.get().strip() or not status_var.get().strip():
            messagebox.showwarning("Cars", "Required fields missing.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO car (car_id, branch_id, license_plate, model_year, car_type, daily_rate, seats, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (int(id_var.get()), hid, room_num_var.get().strip(), int(floor_var.get()), type_var.get(), float(price_var.get()), int(cap_var.get()), status_var.get())
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Cars", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Cars", "Select a car.", parent=frame)
            return
        hid = get_combo_id(hotel_var.get())
        if not hid or not room_num_var.get().strip() or not floor_var.get().strip() or not type_var.get().strip() or not price_var.get().strip() or not cap_var.get().strip() or not status_var.get().strip():
            messagebox.showwarning("Cars", "Required fields missing.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE car SET branch_id=%s, license_plate=%s, model_year=%s, car_type=%s, daily_rate=%s, seats=%s, status=%s WHERE car_id=%s",
                (hid, room_num_var.get().strip(), int(floor_var.get()), type_var.get(), float(price_var.get()), int(cap_var.get()), status_var.get(), int(id_var.get()))
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Cars", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Cars", "Select a car.", parent=frame)
            return
        if not messagebox.askyesno("Cars", "Delete this car?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM car WHERE car_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Cars", "Deleted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=12, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind('<Visibility>', lambda e: refresh())
    return frame
