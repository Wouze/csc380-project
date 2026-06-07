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
    frame.rowconfigure(9, weight=1)

    ttk.Label(frame, text="Payments", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Payment ID").grid(row=1, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w", pady=FIELD_PADY)

    res_var = tk.StringVar()
    ttk.Label(frame, text="Rental *").grid(row=2, column=0, sticky="w", pady=FIELD_PADY)
    res_combo = ttk.Combobox(frame, textvariable=res_var, width=36, state="readonly")
    res_combo.grid(row=2, column=1, sticky="w", pady=FIELD_PADY)

    amt_var = tk.StringVar()
    ttk.Label(frame, text="Total Amount *").grid(row=3, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=amt_var, width=16).grid(row=3, column=1, sticky="w", pady=FIELD_PADY)

    method_var = tk.StringVar()
    ttk.Label(frame, text="Payment Method *").grid(row=4, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=method_var, width=20).grid(row=4, column=1, sticky="w", pady=FIELD_PADY)

    status_var = tk.StringVar()
    ttk.Label(frame, text="Payment Status *").grid(row=5, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=status_var, width=20).grid(row=5, column=1, sticky="w", pady=FIELD_PADY)

    date_var = tk.StringVar()
    ttk.Label(frame, text="Issue Date *").grid(row=6, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=date_var, width=16).grid(row=6, column=1, sticky="w", pady=FIELD_PADY)
    ttk.Label(frame, text="(YYYY-MM-DD)", foreground="gray").grid(row=6, column=2, sticky="w", pady=FIELD_PADY)

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Payment ID)").grid(row=7, column=0, sticky="w", pady=SEARCH_PADY)
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=7, column=1, sticky="w", pady=SEARCH_PADY)

    cols = ("payment_id", "rental_id", "total_amount", "payment_method", "payment_status", "issue_date")
    headings = ("Payment ID", "Rental ID", "Total Amount", "Payment Method", "Payment Status", "Issue Date")
    tree = create_tree_panel(frame, 9, cols, headings, (80, 80, 100, 120, 120, 100))

    def load_combos():
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("SELECT rental_id FROM rental ORDER BY rental_id")
            rows = cur.fetchall()
            cn.close()
            res_combo["values"] = [f"{r[0]} | Rental {r[0]}" for r in rows]
        except Exception:
            pass

    def get_combo_id(val):
        if not val.strip(): return None
        return int(val.split("|")[0].strip())

    def load_row(_e=None):
        sel = tree.selection()
        if not sel: return
        v = tree.item(sel[0], "values")
        id_var.set(str(v[0]))
        rid = str(v[1])
        for val in res_combo["values"]:
            if val.startswith(rid + " |"):
                res_combo.set(val)
                break
        amt_var.set(str(v[2]))
        method_var.set(v[3])
        status_var.set(v[4])
        date_var.set(v[5])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        res_var.set("")
        amt_var.set("")
        method_var.set("")
        status_var.set("")
        date_var.set("")
        search_var.set("")

    def refresh(search=""):
        load_combos()
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search and search.isdigit():
                cur.execute("SELECT payment_id, rental_id, total_amount, payment_method, payment_status, issue_date FROM payment WHERE payment_id = %s", (int(search),))
            else:
                cur.execute("SELECT payment_id, rental_id, total_amount, payment_method, payment_status, issue_date FROM payment ORDER BY payment_id")
            rows = cur.fetchall()
            cn.close()
            fill_tree(tree, rows)
        except Exception as exc:
            show_db_error(frame, exc)

    def do_search():
        refresh(search_var.get().strip())

    def do_insert():
        rid = get_combo_id(res_var.get())
        if not id_var.get().strip() or not rid or not amt_var.get().strip() or not method_var.get().strip() or not status_var.get().strip() or not date_var.get().strip():
            show_warning(frame, "Payments", "Required fields missing.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO payment (payment_id, rental_id, total_amount, payment_method, payment_status, issue_date) VALUES (%s,%s,%s,%s,%s,%s)",
                (int(id_var.get()), rid, float(amt_var.get().strip()), method_var.get().strip(), status_var.get().strip(), date_var.get().strip())
            )
            cn.commit()
            cn.close()
            show_info(frame, "Payments", "Inserted successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            show_warning(frame, "Payments", "Select a record.")
            return
        rid = get_combo_id(res_var.get())
        if not id_var.get().strip() or not rid or not amt_var.get().strip() or not method_var.get().strip() or not status_var.get().strip() or not date_var.get().strip():
            show_warning(frame, "Payments", "Required fields missing.")
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE payment SET rental_id=%s, total_amount=%s, payment_method=%s, payment_status=%s, issue_date=%s WHERE payment_id=%s",
                (rid, float(amt_var.get().strip()), method_var.get().strip(), status_var.get().strip(), date_var.get().strip(), int(id_var.get()))
            )
            cn.commit()
            cn.close()
            show_info(frame, "Payments", "Updated successfully.")
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            show_warning(frame, "Payments", "Select a record.")
            return
        if not ask_yes_no(frame, "Payments", "Delete this payment?"):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM payment WHERE payment_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            show_info(frame, "Payments", "Deleted successfully.")
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=10, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind('<Visibility>', lambda e: refresh())
    return frame
