import tkinter as tk
from decimal import Decimal
from tkinter import messagebox, ttk
from mysql.connector import Error as MySQLError

FIELD_PADY = (0, 6)
SEARCH_PADY = (18, 10)
TREE_ROW_HEIGHT = 24


def setup_tree_style():
    style = ttk.Style()
    style.configure("Treeview", rowheight=TREE_ROW_HEIGHT)


def bind_tree_autosize(tree, min_rows=4):
    def on_configure(event):
        if event.widget is not tree:
            return
        rows = max(min_rows, (tree.winfo_height() - 2) // TREE_ROW_HEIGHT)
        if rows != tree.cget("height"):
            tree.configure(height=rows)

    tree.bind("<Configure>", on_configure)


def format_cell(value):
    if value is None:
        return ""
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, Decimal):
        return f"{value:.2f}"
    return str(value)


def format_row(row):
    return tuple(format_cell(v) for v in row)


def fill_tree(tree, rows):
    clear_tree(tree)
    for row in rows:
        tree.insert("", tk.END, iid=str(row[0]), values=format_row(row))


def set_combo_by_label(combo, label):
    target = str(label).strip()
    for val in combo["values"]:
        if "|" in val and val.split("|", 1)[1].strip() == target:
            combo.set(val)
            return


def show_db_error(owner, exc, title="Database error"):
    messagebox.showerror(title, str(exc), parent=owner)


def clear_tree(tree):
    for iid in tree.get_children():
        tree.delete(iid)


def tree_fill(tree, rows):
    fill_tree(tree, rows)

def parse_int(value, field):
    v = value.strip()
    if not v:
        raise ValueError(f"{field} is required.")
    return int(v)

def parse_optional_int(value):
    v = value.strip()
    if not v:
        return None
    return int(v)

def parse_decimal(value, field):
    v = value.strip()
    if not v:
        raise ValueError(f"{field} is required.")
    float(v)
    return v

