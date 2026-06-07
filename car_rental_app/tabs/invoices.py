import tkinter as tk
from tkinter import ttk

from car_rental_app.db import get_connection
from car_rental_app.tabs.common import (
    FIELD_PADY,
    SEARCH_PADY,
    ask_yes_no,
    create_tree_panel,
    fill_tree,
    show_db_error,
    show_info,
    show_warning,
)


def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(6, weight=1)

    ttk.Label(frame, text="Invoices", font=("", 14, "bold")).grid(
        row=0, column=0, columnspan=3, sticky="w", pady=(0, 8)
    )

    id_var = tk.StringVar()
    ttk.Label(frame, text="Invoice ID").grid(row=1, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w", pady=FIELD_PADY)

    payment_var = tk.StringVar()
    ttk.Label(frame, text="Payment ID *").grid(row=2, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=payment_var, width=12).grid(row=2, column=1, sticky="w", pady=FIELD_PADY)

    number_var = tk.StringVar()
    ttk.Label(frame, text="Invoice Number *").grid(row=3, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=number_var, width=24).grid(row=3, column=1, sticky="w", pady=FIELD_PADY)

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Invoice ID)").grid(row=4, column=0, sticky="w", pady=SEARCH_PADY)
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=4, column=1, sticky="w", pady=SEARCH_PADY)

    cols = ("invoice_id", "payment_id", "invoice_number")
    headings = ("Invoice ID", "Payment ID", "Invoice Number")
    tree = create_tree_panel(frame, 6, cols, headings, (90, 90, 160))

    def load_row(_e=None):
        sel = tree.selection()
        if not sel:
            return
        v = tree.item(sel[0], "values")
        id_var.set(str(v[0]))
        payment_var.set(str(v[1]))
        number_var.set(v[2])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        payment_var.set("")
        number_var.set("")
        search_var.set("")

    def refresh(search=""):
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search and search.isdigit():
                cur.execute(
                    "SELECT invoice_id, payment_id, invoice_number FROM invoice WHERE invoice_id = %s",
                    (int(search),),
                )
            else:
                cur.execute(
                    "SELECT invoice_id, payment_id, invoice_number FROM invoice ORDER BY invoice_id"
                )
            rows = cur.fetchall()
            cn.close()
            fill_tree(tree, rows)
        except Exception as exc:
            show_db_error(frame, exc)

    def do_search():
        refresh(search_var.get().strip())

    def do_insert():
        if not id_var.get().strip() or not payment_var.get().strip() or not number_var.get().strip():
            show_warning(frame, "Invoices", "Required fields missing.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO invoice (invoice_id, payment_id, invoice_number) VALUES (%s,%s,%s)",
                (int(id_var.get()), int(payment_var.get()), number_var.get().strip()),
            )
            cn.commit()
            cn.close()
            show_info(frame, "Invoices", "Inserted successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            show_warning(frame, "Invoices", "Select a record.")
            return
        if not payment_var.get().strip() or not number_var.get().strip():
            show_warning(frame, "Invoices", "Required fields missing.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE invoice SET payment_id=%s, invoice_number=%s WHERE invoice_id=%s",
                (int(payment_var.get()), number_var.get().strip(), int(id_var.get())),
            )
            cn.commit()
            cn.close()
            show_info(frame, "Invoices", "Updated successfully.")
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            show_warning(frame, "Invoices", "Select a record.")
            return
        if not ask_yes_no(frame, "Invoices", "Delete this invoice?"):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM invoice WHERE invoice_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            show_info(frame, "Invoices", "Deleted successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=7, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind("<Visibility>", lambda e: refresh())
    return frame
