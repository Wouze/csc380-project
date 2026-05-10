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
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(9, weight=1)

    ttk.Label(frame, text="Invoices", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")

    inv_id_var = tk.StringVar()
    ttk.Label(frame, text="Invoice ID").grid(row=1, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=inv_id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    res_var = tk.StringVar()
    ttk.Label(frame, text="Reservation *").grid(row=2, column=0, sticky="w", pady=2)
    res_combo = ttk.Combobox(frame, textvariable=res_var, width=40, state="readonly")
    res_combo.grid(row=2, column=1, columnspan=2, sticky="we")

    total_var = tk.StringVar()
    ttk.Label(frame, text="Total amount *").grid(row=3, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=total_var, width=20).grid(row=3, column=1, sticky="w")

    pay_method_var = tk.StringVar(value="Cash")
    ttk.Label(frame, text="Payment method *").grid(row=4, column=0, sticky="w", pady=2)
    ttk.Combobox(
        frame,
        textvariable=pay_method_var,
        values=("Cash", "Credit Card", "Debit Card", "Bank Transfer"),
        width=22,
        state="readonly",
    ).grid(row=4, column=1, sticky="w")

    pay_status_var = tk.StringVar(value="Pending")
    ttk.Label(frame, text="Payment status *").grid(row=5, column=0, sticky="w", pady=2)
    ttk.Combobox(
        frame,
        textvariable=pay_status_var,
        values=("Pending", "Paid", "Failed", "Refunded"),
        width=22,
        state="readonly",
    ).grid(row=5, column=1, sticky="w")

    issue_var = tk.StringVar()
    ttk.Label(frame, text="Issue date *").grid(row=6, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=issue_var, width=18).grid(row=6, column=1, sticky="w")

    ttk.Label(frame, text="YYYY-MM-DD", foreground="gray").grid(row=7, column=1, sticky="w")

    cols = ("invoice_id", "reservation_id", "total_amount", "payment_method", "payment_status", "issue_date")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (70, 90, 100, 120, 120, 100)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=9, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=9, column=4, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def format_res_rows(rows: list[tuple]) -> list[str]:
        """rows: reservation_id, first_name, last_name."""
        return [f"{r[0]} — {r[1]} {r[2]}" for r in rows]

    def load_open_reservations() -> None:
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT r.reservation_id, g.first_name, g.last_name
                    FROM reservation r
                    JOIN guest g ON g.guest_id = r.guest_id
                    LEFT JOIN invoice i ON i.reservation_id = r.reservation_id
                    WHERE i.invoice_id IS NULL
                    ORDER BY r.reservation_id
                    """
                )
                free = cur.fetchall()
            res_combo["values"] = format_res_rows(free)
            res_combo.configure(state="readonly")
            res_var.set("")
        except Exception as exc:
            show_db_error(frame, exc)

    def load_res_combo_for_existing(reservation_id: int) -> None:
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT r.reservation_id, g.first_name, g.last_name
                    FROM reservation r
                    JOIN guest g ON g.guest_id = r.guest_id
                    WHERE r.reservation_id=%s
                    """,
                    (reservation_id,),
                )
                row = cur.fetchone()
                if row:
                    res_combo["values"] = format_res_rows([row])
                    res_combo.set(format_res_rows([row])[0])
            res_combo.configure(state="disabled")
        except Exception as exc:
            show_db_error(frame, exc)

    def clear_form_insert_mode() -> None:
        inv_id_var.set("")
        total_var.set("")
        pay_method_var.set("Cash")
        pay_status_var.set("Pending")
        issue_var.set("")
        load_open_reservations()
        res_combo.configure(state="readonly")

    def load_row(_e=None) -> None:
        sel = tree.selection()
        if not sel:
            return
        v = tree.item(sel[0], "values")
        inv_id_var.set(str(v[0]))
        issue_var.set(str(v[5]))
        total_var.set(str(v[2]))
        pay_method_var.set(v[3])
        pay_status_var.set(v[4])
        rid = int(v[1])
        load_res_combo_for_existing(rid)

    tree.bind("<<TreeviewSelect>>", load_row)

    def refresh() -> None:
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT invoice_id, reservation_id, total_amount, payment_method, payment_status, issue_date
                    FROM invoice
                    ORDER BY invoice_id
                    """
                )
                rows = cur.fetchall()
            clear_tree(tree)
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), values=r)
            clear_form_insert_mode()
            sel_rm = tree.selection()
            if sel_rm:
                tree.selection_remove(*sel_rm)
        except Exception as exc:
            show_db_error(frame, exc)

    def parse_res_id() -> int:
        txt = res_var.get().strip()
        if not txt:
            raise ValueError("Reservation is required.")
        return int(txt.split("—", 1)[0].strip())

    def insert_inv() -> None:
        try:
            if inv_id_var.get().strip():
                messagebox.showinfo("Invoices", "Clear selection to insert.", parent=frame)
                return
            rid = parse_res_id()
            total = parse_decimal(total_var.get(), "Total amount")
            issue_date = _parse_date(issue_var.get(), "Issue date")
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    INSERT INTO invoice (reservation_id, total_amount, payment_method, payment_status, issue_date)
                    VALUES (%s,%s,%s,%s,%s)
                    """,
                    (rid, total, pay_method_var.get(), pay_status_var.get(), issue_date),
                )
                cn.commit()
            messagebox.showinfo("Invoices", "Invoice inserted.", parent=frame)
            refresh()
        except ValueError as ve:
            messagebox.showwarning("Invoices", str(ve), parent=frame)
        except Exception as exc:
            show_db_error(frame, exc)

    def update_inv() -> None:
        iid = inv_id_var.get().strip()
        if not iid:
            messagebox.showwarning("Invoices", "Select an invoice to update.", parent=frame)
            return
        sel_rows = tree.selection()
        if not sel_rows:
            messagebox.showwarning("Invoices", "Select an invoice in the table.", parent=frame)
            return
        vals = tree.item(sel_rows[0], "values")
        rid = int(vals[1])
        try:
            total = parse_decimal(total_var.get(), "Total amount")
            issue_date = _parse_date(issue_var.get(), "Issue date")
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    UPDATE invoice SET total_amount=%s, payment_method=%s, payment_status=%s, issue_date=%s
                    WHERE invoice_id=%s AND reservation_id=%s
                    """,
                    (
                        total,
                        pay_method_var.get(),
                        pay_status_var.get(),
                        issue_date,
                        int(iid),
                        rid,
                    ),
                )
                cn.commit()
            messagebox.showinfo("Invoices", "Invoice updated.", parent=frame)
            refresh()
        except ValueError as ve:
            messagebox.showwarning("Invoices", str(ve), parent=frame)
        except Exception as exc:
            show_db_error(frame, exc)

    def delete_inv() -> None:
        iid = inv_id_var.get().strip()
        if not iid:
            messagebox.showwarning("Invoices", "Select an invoice.", parent=frame)
            return
        if not messagebox.askyesno("Invoices", "Delete this invoice?", parent=frame):
            return
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute("DELETE FROM invoice WHERE invoice_id=%s", (int(iid),))
                cn.commit()
            messagebox.showinfo("Invoices", "Invoice deleted.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btns = ttk.Frame(frame)
    btns.grid(row=8, column=0, columnspan=3, sticky="w", pady=(6, 0))
    ttk.Button(btns, text="Insert", command=insert_inv).pack(side="left", padx=(0, 6))
    ttk.Button(btns, text="Update", command=update_inv).pack(side="left", padx=6)
    ttk.Button(btns, text="Delete", command=delete_inv).pack(side="left", padx=6)
    ttk.Button(btns, text="Refresh", command=refresh).pack(side="left", padx=6)

    # New invoice (unlock reservation combo): user deselect tree + clear isn't obvious — Clear form button:
    def new_invoice_form() -> None:
        sel_rm = tree.selection()
        if sel_rm:
            tree.selection_remove(*sel_rm)
        clear_form_insert_mode()

    ttk.Button(btns, text="New invoice", command=new_invoice_form).pack(side="left", padx=12)

    refresh()
    return frame, refresh
