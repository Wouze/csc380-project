from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Callable, Optional

from mysql.connector import Error as MySQLError
from mysql.connector import errorcode


def show_db_error(owner: tk.Misc, exc: Exception, title: str = "Database error") -> None:
    if isinstance(exc, MySQLError):
        if exc.errno == errorcode.ER_DUP_ENTRY:
            messagebox.showerror(title, "Duplicate value violates a unique constraint.", parent=owner)
            return
        messagebox.showerror(title, str(exc), parent=owner)
        return
    messagebox.showerror(title, str(exc), parent=owner)


def clear_tree(tree: ttk.Treeview) -> None:
    for iid in tree.get_children():
        tree.delete(iid)


def tree_fill(
    tree: ttk.Treeview,
    rows: list[tuple[Any, ...]],
) -> None:
    clear_tree(tree)
    for row in rows:
        iid = str(row[0])
        tree.insert("", tk.END, iid=iid, values=row)


def parse_int(value: str, field: str) -> int:
    v = value.strip()
    if not v:
        raise ValueError(f"{field} is required.")
    return int(v)


def parse_optional_int(value: str) -> Optional[int]:
    v = value.strip()
    if not v:
        return None
    return int(v)


def parse_decimal(value: str, field: str) -> str:
    v = value.strip()
    if not v:
        raise ValueError(f"{field} is required.")
    float(v)  # validate
    return v


TabBuild = tuple[ttk.Frame, Callable[[], None]]
