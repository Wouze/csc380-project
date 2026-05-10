from __future__ import annotations

import datetime as dt
import tkinter as tk
from tkinter import messagebox, ttk

from hotel_app.db import get_connection
from hotel_app.tabs.common import TabBuild, clear_tree, parse_decimal, show_db_error


def _parse_date(s: str, label: str) -> dt.date:
    v = s.strip()
    if not v:
        raise ValueError(f"{label} is required (YYYY-MM-DD).")
    return dt.datetime.strptime(v, "%Y-%m-%d").date()


def build(parent: tk.Misc) -> TabBuild:
    frame = ttk.Frame(parent, padding=8)

    paned = ttk.Panedwindow(frame, orient="horizontal")
    paned.pack(fill="both", expand=True)

    left = ttk.Frame(paned, padding=(0, 0, 8, 0))
    paned.add(left, weight=1)

    right = ttk.Frame(paned, padding=(8, 0, 0, 0))
    paned.add(right, weight=1)

    ttk.Label(left, text="Reservations", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")

    res_id_var = tk.StringVar()
    ttk.Label(left, text="Reservation ID").grid(row=1, column=0, sticky="nw", pady=2)
    ttk.Entry(left, textvariable=res_id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    booking_var = tk.StringVar()
    ttk.Label(left, text="Booking date *").grid(row=2, column=0, sticky="nw", pady=2)
    ttk.Entry(left, textvariable=booking_var, width=16).grid(row=2, column=1, sticky="w")

    in_var = tk.StringVar()
    ttk.Label(left, text="Check-in *").grid(row=3, column=0, sticky="nw", pady=2)
    ttk.Entry(left, textvariable=in_var, width=16).grid(row=3, column=1, sticky="w")

    out_var = tk.StringVar()
    ttk.Label(left, text="Check-out *").grid(row=4, column=0, sticky="nw", pady=2)
    ttk.Entry(left, textvariable=out_var, width=16).grid(row=4, column=1, sticky="w")

    status_var = tk.StringVar(value="confirmed")
    ttk.Label(left, text="Status *").grid(row=5, column=0, sticky="nw", pady=2)
    ttk.Combobox(
        left,
        textvariable=status_var,
        values=("confirmed", "checked-in", "checked-out", "cancelled"),
        width=18,
        state="readonly",
    ).grid(row=5, column=1, sticky="w")

    guest_var = tk.StringVar()
    ttk.Label(left, text="Guest *").grid(row=6, column=0, sticky="nw", pady=2)
    guest_combo = ttk.Combobox(left, textvariable=guest_var, width=28, state="readonly")
    guest_combo.grid(row=6, column=1, columnspan=2, sticky="we")

    ttk.Label(left, text="(Dates: YYYY-MM-DD)", foreground="gray").grid(row=7, column=1, sticky="w")

    def load_guests_combo() -> None:
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT guest_id, first_name, last_name
                    FROM guest
                    ORDER BY guest_id
                    """
                )
                rows = cur.fetchall()
            guest_combo["values"] = [f"{r[0]} — {r[1]} {r[2]}" for r in rows]
        except Exception as exc:
            show_db_error(left, exc)

    def parse_guest_id() -> int:
        txt = guest_var.get().strip()
        if not txt:
            raise ValueError("Guest is required.")
        return int(txt.split("—", 1)[0].strip())

    cols = ("reservation_id", "guest_id", "booking_date", "check_in_date", "check_out_date", "status")
    res_tree = ttk.Treeview(left, columns=cols, show="headings", height=10)
    for c, w in zip(cols, (90, 60, 100, 100, 100, 100)):
        res_tree.heading(c, text=c.replace("_", " ").title())
        res_tree.column(c, width=w, anchor="w")
    res_tree.grid(row=9, column=0, columnspan=3, sticky="nsew", pady=8)

    yr = ttk.Scrollbar(left, orient="vertical", command=res_tree.yview)
    yr.grid(row=9, column=3, sticky="ns", pady=8)
    res_tree.configure(yscrollcommand=yr.set)
    left.rowconfigure(9, weight=1)
    left.columnconfigure(1, weight=1)

    def clear_res_form() -> None:
        res_id_var.set("")
        booking_var.set("")
        in_var.set("")
        out_var.set("")
        status_var.set("confirmed")
        guest_var.set("")

    def rr_refresh_for(reservation_id: int | None) -> None:
        clear_tree(rr_tree)
        if reservation_id is None:
            return
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT rr.room_id, r.room_number, rr.price_at_booking, r.hotel_id
                    FROM reservation_room rr
                    JOIN room r ON r.room_id = rr.room_id
                    WHERE rr.reservation_id = %s
                    ORDER BY rr.room_id
                    """,
                    (reservation_id,),
                )
                rows = cur.fetchall()
            for r in rows:
                rr_tree.insert("", tk.END, iid=str(r[0]), values=r)
        except Exception as exc:
            show_db_error(right, exc)

    def load_res_row(_e=None) -> None:
        sel = res_tree.selection()
        if not sel:
            rr_refresh_for(None)
            return
        v = res_tree.item(sel[0], "values")
        res_id_var.set(str(v[0]))
        gid = str(v[1])
        guest_combo.set(next((x for x in guest_combo["values"] if x.startswith(gid + " —")), ""))
        booking_var.set(str(v[2]))
        in_var.set(str(v[3]))
        out_var.set(str(v[4]))
        status_var.set(v[5])
        rr_refresh_for(int(v[0]))

    res_tree.bind("<<TreeviewSelect>>", load_res_row)

    def refresh_reservations() -> None:
        load_guests_combo()
        load_hotels_rr()
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT reservation_id, guest_id, booking_date, check_in_date, check_out_date, status
                    FROM reservation
                    ORDER BY reservation_id
                    """
                )
                rows = cur.fetchall()
            clear_tree(res_tree)
            for r in rows:
                res_tree.insert("", tk.END, iid=str(r[0]), values=r)
            clear_res_form()
            rr_refresh_for(None)
        except Exception as exc:
            show_db_error(left, exc)

    def validate_dates(booking_date: dt.date, check_in_date: dt.date, check_out_date: dt.date) -> bool:
        if check_in_date > check_out_date:
            messagebox.showwarning(
                "Reservations",
                "Check-in date must be on or before check-out date.",
                parent=left,
            )
            return False
        if booking_date > check_in_date:
            messagebox.showwarning(
                "Reservations",
                "Booking date must be on or before check-in date.",
                parent=left,
            )
            return False
        return True

    def insert_reservation() -> None:
        try:
            b = _parse_date(booking_var.get(), "Booking date")
            ci = _parse_date(in_var.get(), "Check-in date")
            co = _parse_date(out_var.get(), "Check-out date")
            if not validate_dates(b, ci, co):
                return
            gid = parse_guest_id()
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    INSERT INTO reservation (booking_date, check_in_date, check_out_date, status, guest_id)
                    VALUES (%s,%s,%s,%s,%s)
                    """,
                    (b, ci, co, status_var.get(), gid),
                )
                cn.commit()
            messagebox.showinfo("Reservations", "Reservation created.", parent=left)
            refresh_reservations()
        except ValueError as ve:
            messagebox.showwarning("Reservations", str(ve), parent=left)
        except Exception as exc:
            show_db_error(left, exc)

    def update_reservation() -> None:
        rid = res_id_var.get().strip()
        if not rid:
            messagebox.showwarning("Reservations", "Select a reservation to update.", parent=left)
            return
        try:
            b = _parse_date(booking_var.get(), "Booking date")
            ci = _parse_date(in_var.get(), "Check-in date")
            co = _parse_date(out_var.get(), "Check-out date")
            if not validate_dates(b, ci, co):
                return
            gid = parse_guest_id()
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    UPDATE reservation
                    SET booking_date=%s, check_in_date=%s, check_out_date=%s, status=%s, guest_id=%s
                    WHERE reservation_id=%s
                    """,
                    (b, ci, co, status_var.get(), gid, int(rid)),
                )
                cn.commit()
            messagebox.showinfo("Reservations", "Reservation updated.", parent=left)
            refresh_reservations()
        except ValueError as ve:
            messagebox.showwarning("Reservations", str(ve), parent=left)
        except Exception as exc:
            show_db_error(left, exc)

    def delete_reservation() -> None:
        rid = res_id_var.get().strip()
        if not rid:
            messagebox.showwarning("Reservations", "Select a reservation to delete.", parent=left)
            return
        if not messagebox.askyesno(
            "Reservations",
            "Delete this reservation? (Clears junction rows via CASCADE; invoice may block.)",
            parent=left,
        ):
            return
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute("DELETE FROM reservation WHERE reservation_id=%s", (int(rid),))
                cn.commit()
            messagebox.showinfo("Reservations", "Reservation deleted.", parent=left)
            refresh_reservations()
        except Exception as exc:
            show_db_error(left, exc)

    rb = ttk.Frame(left)
    rb.grid(row=10, column=0, columnspan=3, sticky="w")
    ttk.Button(rb, text="Insert", command=insert_reservation).pack(side="left", padx=(0, 6))
    ttk.Button(rb, text="Update", command=update_reservation).pack(side="left", padx=6)
    ttk.Button(rb, text="Delete", command=delete_reservation).pack(side="left", padx=6)
    ttk.Button(rb, text="Refresh", command=refresh_reservations).pack(side="left", padx=6)

    ttk.Label(right, text="Rooms on reservation", font=("", 13, "bold")).grid(row=0, column=0, columnspan=4, sticky="w")
    ttk.Label(
        right,
        text="Pick a hotel to filter rooms (schema has no reservation→hotel FK).",
        foreground="gray",
    ).grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 6))

    hotel_rr_var = tk.StringVar()
    ttk.Label(right, text="Hotel context").grid(row=2, column=0, sticky="nw", pady=2)
    hotel_rr_combo = ttk.Combobox(right, textvariable=hotel_rr_var, width=34, state="readonly")
    hotel_rr_combo.grid(row=2, column=1, columnspan=3, sticky="we", pady=2)

    room_pick_var = tk.StringVar()
    ttk.Label(right, text="Room *").grid(row=3, column=0, sticky="nw", pady=2)
    room_pick_combo = ttk.Combobox(right, textvariable=room_pick_var, width=34, state="readonly")
    room_pick_combo.grid(row=3, column=1, columnspan=3, sticky="we", pady=2)

    rr_price_var = tk.StringVar()
    ttk.Label(right, text="Price at booking *").grid(row=4, column=0, sticky="nw", pady=2)
    ttk.Entry(right, textvariable=rr_price_var, width=16).grid(row=4, column=1, sticky="w")

    rr_cols = ("room_id", "room_number", "price_at_booking", "hotel_id")
    rr_tree = ttk.Treeview(right, columns=rr_cols, show="headings", height=8)
    for c, w in zip(rr_cols, (70, 100, 120, 60)):
        rr_tree.heading(c, text=c.replace("_", " ").title())
        rr_tree.column(c, width=w, anchor="w")
    rr_tree.grid(row=7, column=0, columnspan=4, sticky="nsew", pady=8)

    rr_y = ttk.Scrollbar(right, orient="vertical", command=rr_tree.yview)
    rr_y.grid(row=7, column=4, sticky="ns", pady=8)
    rr_tree.configure(yscrollcommand=rr_y.set)
    right.rowconfigure(7, weight=1)
    right.columnconfigure(1, weight=1)

    def parse_hotel_id_rr() -> int:
        txt = hotel_rr_var.get().strip()
        if not txt:
            raise ValueError("Select hotel context.")
        return int(txt.split("—", 1)[0].strip())

    def parse_room_pick_id() -> int:
        txt = room_pick_var.get().strip()
        if not txt:
            raise ValueError("Select a room.")
        return int(txt.split("—", 1)[0].strip())

    def load_hotels_rr() -> None:
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute("SELECT hotel_id, name FROM hotel ORDER BY hotel_id")
                rows = cur.fetchall()
            hotel_rr_combo["values"] = [f"{r[0]} — {r[1]}" for r in rows]
            if hotel_rr_combo["values"] and not hotel_rr_var.get():
                hotel_rr_combo.current(0)
            refresh_rooms_for_hotel()
        except Exception as exc:
            show_db_error(right, exc)

    def refresh_rooms_for_hotel(_e=None) -> None:
        try:
            hid = parse_hotel_id_rr()
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT room_id, room_number, room_type, price_per_night
                    FROM room
                    WHERE hotel_id=%s
                    ORDER BY room_number
                    """,
                    (hid,),
                )
                rows = cur.fetchall()
            room_pick_combo["values"] = [
                f"{r[0]} — #{r[1]} ({r[2]}, {r[3]}/night)" for r in rows
            ]
            if room_pick_combo["values"]:
                room_pick_combo.current(0)
            else:
                room_pick_var.set("")
        except ValueError:
            room_pick_combo["values"] = []
            room_pick_var.set("")
        except Exception as exc:
            show_db_error(right, exc)

    hotel_rr_combo.bind("<<ComboboxSelected>>", refresh_rooms_for_hotel)

    def rr_add_line() -> None:
        rid = res_id_var.get().strip()
        if not rid:
            messagebox.showwarning("Reservations", "Select a reservation first.", parent=right)
            return
        try:
            roid = parse_room_pick_id()
            price = parse_decimal(rr_price_var.get(), "Price at booking")
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    INSERT INTO reservation_room (reservation_id, room_id, price_at_booking)
                    VALUES (%s,%s,%s)
                    """,
                    (int(rid), roid, price),
                )
                cn.commit()
            messagebox.showinfo("Reservations", "Room line added.", parent=right)
            rr_refresh_for(int(rid))
        except ValueError as ve:
            messagebox.showwarning("Reservations", str(ve), parent=right)
        except Exception as exc:
            show_db_error(right, exc)

    def rr_delete_line() -> None:
        rid = res_id_var.get().strip()
        if not rid:
            messagebox.showwarning("Reservations", "Select a reservation.", parent=right)
            return
        sel = rr_tree.selection()
        if not sel:
            messagebox.showwarning("Reservations", "Select a room line to remove.", parent=right)
            return
        room_id = sel[0]
        if not messagebox.askyesno("Reservations", "Remove this room from the reservation?", parent=right):
            return
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    "DELETE FROM reservation_room WHERE reservation_id=%s AND room_id=%s",
                    (int(rid), int(room_id)),
                )
                cn.commit()
            messagebox.showinfo("Reservations", "Room line removed.", parent=right)
            rr_refresh_for(int(rid))
        except Exception as exc:
            show_db_error(right, exc)

    rrb = ttk.Frame(right)
    rrb.grid(row=5, column=0, columnspan=4, sticky="w", pady=(4, 0))
    ttk.Button(rrb, text="Add room to reservation", command=rr_add_line).pack(side="left", padx=(0, 8))
    ttk.Button(rrb, text="Remove selected line", command=rr_delete_line).pack(side="left")

    refresh_reservations()
    return frame, refresh_reservations
