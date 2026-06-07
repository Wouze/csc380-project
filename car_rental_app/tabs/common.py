import tkinter as tk
from decimal import Decimal
from tkinter import ttk
from mysql.connector import Error as MySQLError

FIELD_PADY = (0, 6)
SEARCH_PADY = (18, 10)
TREE_ROW_HEIGHT = 34
TREE_VISIBLE_ROWS = 12
DIALOG_FONT = ("", 12)
DIALOG_TITLE_FONT = ("", 13, "bold")
DIALOG_WRAP = 460
DIALOG_MIN_WIDTH = 480
DIALOG_MIN_HEIGHT = 170
DIALOG_PAD = 24


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


def _center_dialog(dialog, parent):
    dialog.update_idletasks()
    root = parent.winfo_toplevel()
    x = root.winfo_rootx() + max((root.winfo_width() - dialog.winfo_width()) // 2, 0)
    y = root.winfo_rooty() + max((root.winfo_height() - dialog.winfo_height()) // 2, 0)
    dialog.geometry(f"+{x}+{y}")


def _show_dialog(parent, title, message, buttons):
    dialog = tk.Toplevel(parent)
    dialog.title(title)
    dialog.transient(parent.winfo_toplevel())
    dialog.grab_set()
    dialog.resizable(True, True)
    dialog.minsize(DIALOG_MIN_WIDTH, DIALOG_MIN_HEIGHT)

    frame = ttk.Frame(dialog, padding=DIALOG_PAD)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text=title, font=DIALOG_TITLE_FONT).pack(anchor="w", pady=(0, 10))
    ttk.Label(
        frame,
        text=message,
        font=DIALOG_FONT,
        wraplength=DIALOG_WRAP,
        justify="left",
    ).pack(fill="both", expand=True, pady=(0, 18))

    result = {"value": buttons[-1][1]}
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(anchor="e")

    def close(value):
        result["value"] = value
        dialog.destroy()

    for label, value in buttons:
        ttk.Button(btn_frame, text=label, width=10, command=lambda v=value: close(v)).pack(
            side="left", padx=4
        )

    dialog.bind("<Escape>", lambda _e: close(buttons[-1][1]))
    _center_dialog(dialog, parent)
    dialog.wait_window()
    return result["value"]


def show_info(parent, title, message):
    _show_dialog(parent, title, message, [("OK", True)])


def show_warning(parent, title, message):
    _show_dialog(parent, title, message, [("OK", True)])


def show_error(parent, title, message):
    _show_dialog(parent, title, message, [("OK", True)])


def ask_yes_no(parent, title, message):
    return _show_dialog(parent, title, message, [("Yes", True), ("No", False)])


def show_db_error(owner, exc, title="Database error"):
    show_error(owner, title, str(exc))


def block_delete_if_linked(frame, title, cursor, count_sql, params, item_label):
    cursor.execute(count_sql, params)
    count = cursor.fetchone()[0]
    if not count:
        return False
    noun = item_label if count == 1 else f"{item_label}s"
    show_warning(
        frame,
        title,
        f"Cannot delete — {count} linked {noun}.\nRemove or reassign them first.",
    )
    return True


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

