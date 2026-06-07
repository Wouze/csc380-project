import tkinter as tk
from tkinter import messagebox, ttk
from mysql.connector import Error as MySQLError

FIELD_PADY = (0, 6)
SEARCH_PADY = (18, 10)


def show_db_error(owner, exc, title="Database error"):
    messagebox.showerror(title, str(exc), parent=owner)

def clear_tree(tree):
    for iid in tree.get_children():
        tree.delete(iid)

def tree_fill(tree, rows):
    clear_tree(tree)
    for row in rows:
        iid = str(row[0])
        tree.insert("", tk.END, iid=iid, values=row)

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

