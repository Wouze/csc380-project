"""
Hotel Management System — Tkinter + MySQL.

Run from `python-hotel-project/`:
  export HOTEL_DB_HOST=127.0.0.1 HOTEL_DB_NAME=hotel_management HOTEL_DB_USER=root HOTEL_DB_PASSWORD=...
  python -m hotel_app.main
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from hotel_app.db import get_connection
from hotel_app.tabs import employees, guests, hotels, invoices, reservations, rooms


def ping_db() -> None:
    try:
        with get_connection() as cn:
            cur = cn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
    except Exception as exc:
        messagebox.showerror(
            "Hotel Management System",
            f"Cannot connect to MySQL ({exc})\nCheck env: HOTEL_DB_HOST HOTEL_DB_PORT HOTEL_DB_NAME HOTEL_DB_USER HOTEL_DB_PASSWORD.",
        )
        raise SystemExit(1) from exc


def main() -> None:
    ping_db()

    root = tk.Tk()
    root.title("Hotel Management System")
    root.geometry("1100x720")
    root.minsize(900, 560)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    tab_specs: list[tuple[str, Callable[..., tuple[tk.Widget, Callable[[], None]]]]] = [
        ("Hotels", hotels.build),
        ("Rooms", rooms.build),
        ("Guests", guests.build),
        ("Reservations", reservations.build),
        ("Invoices", invoices.build),
        ("Employees", employees.build),
    ]

    refresher_by_index: list[Callable[[], None]] = []

    for title, builder in tab_specs:
        frame, refresh_fn = builder(notebook)
        notebook.add(frame, text=title)
        refresher_by_index.append(refresh_fn)

    def on_tab_changed(_event=None) -> None:
        try:
            idx = notebook.index(notebook.select())
        except tk.TclError:
            return
        try:
            refresher_by_index[idx]()
        except Exception as exc:
            messagebox.showerror("Hotel Management System", str(exc))

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    root.mainloop()


if __name__ == "__main__":
    main()
