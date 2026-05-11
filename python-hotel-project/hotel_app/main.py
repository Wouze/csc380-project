"""
Hotel Management System — Tkinter + MySQL.

Run from `python-hotel-project/`:
  python -m hotel_app.main

Defaults match a typical XAMPP install (MySQL on 127.0.0.1:3306, user root, empty password,
database hotel_management). On first launch the app creates the database and tables if needed.

To reset all tables manually: python create_schema.py
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from hotel_app.config import settings
from hotel_app.schema_setup import ensure_ready_for_app
from hotel_app.tabs import employees, guests, hotels, invoices, reservations, rooms


def ping_db(parent: tk.Misc) -> None:
    try:
        did_setup = ensure_ready_for_app()
        if did_setup:
            messagebox.showinfo(
                "Hotel Management System",
                "First-time database setup finished.\n\n"
                f'Database "{settings.database}" is ready (schema applied).\n'
                "Connection defaults: 127.0.0.1 port 3306, user root — typical for XAMPP.",
                parent=parent,
            )
    except Exception as exc:
        messagebox.showerror(
            "Hotel Management System",
            "Cannot connect to MySQL or apply the schema.\n\n"
            f"{exc}\n\n"
            "Check that XAMPP **MySQL** is started (port **3306**).\n"
            "Defaults: user **root**, empty password, database **hotel_management**.\n"
            "Override with HOTEL_DB_* env vars, or run: python create_schema.py",
            parent=parent,
        )
        raise SystemExit(1) from exc


def main() -> None:
    root = tk.Tk()
    root.withdraw()
    ping_db(root)
    root.deiconify()

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
