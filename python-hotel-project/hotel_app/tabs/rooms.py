from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from hotel_app.db import get_connection
from hotel_app.tabs.common import TabBuild, clear_tree, parse_decimal, show_db_error


def build(parent: tk.Misc) -> TabBuild:
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)

    ttk.Label(frame, text="Rooms", font=("", 14, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

    ttk.Label(frame, text="Room ID (auto)").grid(row=1, column=0, sticky="w")
    room_id_var = tk.StringVar()
    ttk.Entry(frame, textvariable=room_id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    ttk.Label(frame, text="Hotel *").grid(row=2, column=0, sticky="w")
    hotel_var = tk.StringVar()
    hotel_combo = ttk.Combobox(frame, textvariable=hotel_var, width=36, state="readonly")
    hotel_combo.grid(row=2, column=1, columnspan=2, sticky="we")

    def load_hotels_combo() -> None:
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute("SELECT hotel_id, name FROM hotel ORDER BY hotel_id")
                rows = cur.fetchall()
            hotel_combo["values"] = [f"{r[0]} — {r[1]}" for r in rows]
            if hotel_combo["values"] and not hotel_var.get():
                hotel_combo.current(0)
        except Exception as exc:
            show_db_error(frame, exc)

    ttk.Label(frame, text="Room number *").grid(row=3, column=0, sticky="w")
    room_number_var = tk.StringVar()
    ttk.Entry(frame, textvariable=room_number_var, width=20).grid(row=3, column=1, sticky="w")

    ttk.Label(frame, text="Floor *").grid(row=4, column=0, sticky="w")
    floor_var = tk.StringVar()
    ttk.Entry(frame, textvariable=floor_var, width=12).grid(row=4, column=1, sticky="w")

    ttk.Label(frame, text="Type *").grid(row=5, column=0, sticky="w")
    room_type_var = tk.StringVar(value="Single")
    ttk.Combobox(
        frame,
        textvariable=room_type_var,
        values=("Single", "Double", "Suite"),
        width=18,
        state="readonly",
    ).grid(row=5, column=1, sticky="w")

    ttk.Label(frame, text="Price / night *").grid(row=6, column=0, sticky="w")
    price_var = tk.StringVar()
    ttk.Entry(frame, textvariable=price_var, width=16).grid(row=6, column=1, sticky="w")

    ttk.Label(frame, text="Max capacity *").grid(row=7, column=0, sticky="w")
    cap_var = tk.StringVar()
    ttk.Entry(frame, textvariable=cap_var, width=12).grid(row=7, column=1, sticky="w")

    ttk.Label(frame, text="Status *").grid(row=8, column=0, sticky="w")
    status_var = tk.StringVar(value="Available")
    ttk.Combobox(
        frame,
        textvariable=status_var,
        values=("Available", "Occupied", "Maintenance"),
        width=18,
        state="readonly",
    ).grid(row=8, column=1, sticky="w")

    cols = (
        "room_id",
        "hotel_id",
        "room_number",
        "floor",
        "room_type",
        "price_per_night",
        "max_capacity",
        "status",
    )
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (60, 60, 90, 50, 80, 90, 80, 90)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=1, column=3, rowspan=9, sticky="nsew", padx=(16, 0))
    frame.rowconfigure(8, weight=1)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=1, column=4, rowspan=9, sticky="ns", padx=(0, 4))
    tree.configure(yscrollcommand=scroll.set)

    def parse_hotel_id() -> int:
        text = hotel_var.get().strip()
        if not text:
            raise ValueError("Hotel is required.")
        return int(text.split("—", 1)[0].strip())

    def fill_from_row(_evt=None) -> None:
        sel = tree.selection()
        if not sel:
            return
        v = tree.item(sel[0], "values")
        room_id_var.set(str(v[0]))
        hid = str(v[1])
        hotel_combo.set(next((x for x in hotel_combo["values"] if x.startswith(hid + " —")), ""))
        room_number_var.set(v[2])
        floor_var.set(str(v[3]))
        room_type_var.set(v[4])
        price_var.set(str(v[5]))
        cap_var.set(str(v[6]))
        status_var.set(v[7])

    tree.bind("<<TreeviewSelect>>", fill_from_row)

    def clear_form() -> None:
        room_id_var.set("")
        room_number_var.set("")
        floor_var.set("")
        price_var.set("")
        cap_var.set("")
        hotel_var.set("")

    def refresh() -> None:
        load_hotels_combo()
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT room_id, hotel_id, room_number, floor, room_type,
                           price_per_night, max_capacity, status
                    FROM room
                    ORDER BY hotel_id, room_number
                    """
                )
                rows = cur.fetchall()
            clear_tree(tree)
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), values=r)
            clear_form()
        except Exception as exc:
            show_db_error(frame, exc)

    def insert_room() -> None:
        try:
            hid = parse_hotel_id()
            rn = room_number_var.get().strip()
            if not rn:
                messagebox.showwarning("Rooms", "Room number is required.", parent=frame)
                return
            fl = int(floor_var.get().strip())
            price = parse_decimal(price_var.get(), "Price")
            cap = int(cap_var.get().strip())
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    INSERT INTO room
                    (room_number, floor, room_type, price_per_night, max_capacity, status, hotel_id)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (rn, fl, room_type_var.get(), price, cap, status_var.get(), hid),
                )
                cn.commit()
            messagebox.showinfo("Rooms", "Room inserted.", parent=frame)
            refresh()
        except ValueError as ve:
            messagebox.showwarning("Rooms", str(ve), parent=frame)
        except Exception as exc:
            show_db_error(frame, exc)

    def update_room() -> None:
        try:
            rid = room_id_var.get().strip()
            if not rid:
                messagebox.showwarning("Rooms", "Select a room to update.", parent=frame)
                return
            hid = parse_hotel_id()
            rn = room_number_var.get().strip()
            fl = int(floor_var.get().strip())
            price = parse_decimal(price_var.get(), "Price")
            cap = int(cap_var.get().strip())
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    UPDATE room SET room_number=%s, floor=%s, room_type=%s, price_per_night=%s,
                           max_capacity=%s, status=%s, hotel_id=%s
                    WHERE room_id=%s
                    """,
                    (rn, fl, room_type_var.get(), price, cap, status_var.get(), hid, int(rid)),
                )
                cn.commit()
            messagebox.showinfo("Rooms", "Room updated.", parent=frame)
            refresh()
        except ValueError as ve:
            messagebox.showwarning("Rooms", str(ve), parent=frame)
        except Exception as exc:
            show_db_error(frame, exc)

    def delete_room() -> None:
        rid = room_id_var.get().strip()
        if not rid:
            messagebox.showwarning("Rooms", "Select a room to delete.", parent=frame)
            return
        if not messagebox.askyesno("Rooms", "Delete this room?", parent=frame):
            return
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute("DELETE FROM room WHERE room_id=%s", (int(rid),))
                cn.commit()
            messagebox.showinfo("Rooms", "Room deleted.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btns = ttk.Frame(frame)
    btns.grid(row=9, column=0, columnspan=3, sticky="w", pady=(8, 0))
    ttk.Button(btns, text="Insert", command=insert_room).pack(side="left", padx=(0, 6))
    ttk.Button(btns, text="Update", command=update_room).pack(side="left", padx=6)
    ttk.Button(btns, text="Delete", command=delete_room).pack(side="left", padx=6)
    ttk.Button(btns, text="Refresh", command=refresh).pack(side="left", padx=6)

    refresh()
    return frame, refresh
