import tkinter as tk
from decimal import Decimal
from tkinter import messagebox, ttk
from mysql.connector import Error as MySQLError

FIELD_PADY = (0, 6)
SEARCH_PADY = (18, 10)
TREE_ROW_HEIGHT = 34
TREE_VISIBLE_ROWS = 12


def setup_tree_style():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("Treeview", rowheight=TREE_ROW_HEIGHT)
    style.configure("Treeview.Heading", font=("", 10, "bold"))


def create_tree_panel(parent, row, cols, headings, widths, visible_rows=TREE_VISIBLE_ROWS):
    """Table area grows with the window; rows keep a fixed pixel height."""
    parent.rowconfigure(row, weight=1)
    panel = ttk.Frame(parent)
    panel.grid(row=row, column=0, columnspan=3, sticky="nsew", pady=8)
    panel.columnconfigure(0, weight=1)

    tree = ttk.Treeview(panel, columns=cols, show="headings", height=visible_rows, selectmode="browse")
    for col, heading, width in zip(cols, headings, widths):
        tree.heading(col, text=heading)
        tree.column(col, width=width, minwidth=50, anchor="w", stretch=True)
    tree.grid(row=0, column=0, sticky="ew")

    scroll = ttk.Scrollbar(panel, orient="vertical", command=tree.yview)
    scroll.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scroll.set)
    return tree


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
    children = tree.get_children()
    if children:
        tree.delete(*children)


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

