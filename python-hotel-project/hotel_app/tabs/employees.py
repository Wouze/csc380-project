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
    frame.rowconfigure(9, weight=1)  # tree row expands

    ttk.Label(frame, text="Employees", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")

    emp_id_var = tk.StringVar()
    ttk.Label(frame, text="Employee ID").grid(row=1, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=emp_id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    fn_var = tk.StringVar()
    ttk.Label(frame, text="First name *").grid(row=2, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=fn_var, width=28).grid(row=2, column=1, sticky="we")

    ln_var = tk.StringVar()
    ttk.Label(frame, text="Last name *").grid(row=3, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=ln_var, width=28).grid(row=3, column=1, sticky="we")

    role_var = tk.StringVar()
    ttk.Label(frame, text="Role *").grid(row=4, column=0, sticky="w", pady=2)
    ttk.Combobox(
        frame,
        textvariable=role_var,
        values=("Receptionist", "Housekeeper", "Manager", "Chef", "Security", "Maintenance"),
        width=25,
        state="readonly",
    ).grid(row=4, column=1, sticky="w")

    sal_var = tk.StringVar()
    ttk.Label(frame, text="Salary *").grid(row=5, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=sal_var, width=16).grid(row=5, column=1, sticky="w")

    hire_var = tk.StringVar()
    ttk.Label(frame, text="Hire date *").grid(row=6, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=hire_var, width=16).grid(row=6, column=1, sticky="w")
    ttk.Label(frame, text="YYYY-MM-DD", foreground="gray").grid(row=6, column=2, sticky="w", padx=6)

    hotel_var = tk.StringVar()
    ttk.Label(frame, text="Hotel *").grid(row=7, column=0, sticky="w", pady=2)
    hotel_combo = ttk.Combobox(frame, textvariable=hotel_var, width=36, state="readonly")
    hotel_combo.grid(row=7, column=1, sticky="we")

    cols = ("employee_id", "first_name", "last_name", "role", "salary", "hire_date", "hotel_id")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (75, 100, 100, 110, 90, 100, 70)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=9, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=9, column=4, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def parse_hotel_id() -> int:
        txt = hotel_var.get().strip()
        if not txt:
            raise ValueError("Hotel is required.")
        return int(txt.split("—", 1)[0].strip())

    def load_hotels() -> None:
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute("SELECT hotel_id, name FROM hotel ORDER BY hotel_id")
                rows = cur.fetchall()
            hotel_combo["values"] = [f"{r[0]} — {r[1]}" for r in rows]
        except Exception as exc:
            show_db_error(frame, exc)

    def clear_form() -> None:
        emp_id_var.set("")
        fn_var.set("")
        ln_var.set("")
        role_var.set("Receptionist")
        sal_var.set("")
        hire_var.set("")
        hotel_var.set("")

    def fill_row(_e=None) -> None:
        sel = tree.selection()
        if not sel:
            return
        v = tree.item(sel[0], "values")
        emp_id_var.set(str(v[0]))
        fn_var.set(v[1])
        ln_var.set(v[2])
        role_var.set(v[3])
        sal_var.set(str(v[4]))
        hire_var.set(str(v[5]))
        hid = str(v[6])
        hotel_combo.set(next((x for x in hotel_combo["values"] if x.startswith(hid + " —")), ""))

    tree.bind("<<TreeviewSelect>>", fill_row)

    def refresh() -> None:
        load_hotels()
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    SELECT employee_id, first_name, last_name, role, salary, hire_date, hotel_id
                    FROM employee
                    ORDER BY employee_id
                    """
                )
                rows = cur.fetchall()
            clear_tree(tree)
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), values=r)
            clear_form()
        except Exception as exc:
            show_db_error(frame, exc)

    def insert() -> None:
        try:
            sal = parse_decimal(sal_var.get(), "Salary")
            hd = _parse_date(hire_var.get(), "Hire date")
            hid = parse_hotel_id()
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    INSERT INTO employee (first_name, last_name, role, salary, hire_date, hotel_id)
                    VALUES (%s,%s,%s,%s,%s,%s)
                    """,
                    (fn_var.get().strip(), ln_var.get().strip(), role_var.get(), sal, hd, hid),
                )
                cn.commit()
            messagebox.showinfo("Employees", "Employee inserted.", parent=frame)
            refresh()
        except ValueError as ve:
            messagebox.showwarning("Employees", str(ve), parent=frame)
        except Exception as exc:
            show_db_error(frame, exc)

    def update_row() -> None:
        iid = emp_id_var.get().strip()
        if not iid:
            messagebox.showwarning("Employees", "Select an employee to update.", parent=frame)
            return
        try:
            sal = parse_decimal(sal_var.get(), "Salary")
            hd = _parse_date(hire_var.get(), "Hire date")
            hid = parse_hotel_id()
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute(
                    """
                    UPDATE employee SET first_name=%s, last_name=%s, role=%s, salary=%s, hire_date=%s, hotel_id=%s
                    WHERE employee_id=%s
                    """,
                    (
                        fn_var.get().strip(),
                        ln_var.get().strip(),
                        role_var.get(),
                        sal,
                        hd,
                        hid,
                        int(iid),
                    ),
                )
                cn.commit()
            messagebox.showinfo("Employees", "Employee updated.", parent=frame)
            refresh()
        except ValueError as ve:
            messagebox.showwarning("Employees", str(ve), parent=frame)
        except Exception as exc:
            show_db_error(frame, exc)

    def delete_row() -> None:
        iid = emp_id_var.get().strip()
        if not iid:
            messagebox.showwarning("Employees", "Select an employee to delete.", parent=frame)
            return
        if not messagebox.askyesno("Employees", "Delete this employee?", parent=frame):
            return
        try:
            with get_connection() as cn:
                cur = cn.cursor()
                cur.execute("DELETE FROM employee WHERE employee_id=%s", (int(iid),))
                cn.commit()
            messagebox.showinfo("Employees", "Employee deleted.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btns = ttk.Frame(frame)
    btns.grid(row=10, column=0, columnspan=3, sticky="w")
    ttk.Button(btns, text="Insert", command=insert).pack(side="left", padx=(0, 6))
    ttk.Button(btns, text="Update", command=update_row).pack(side="left", padx=6)
    ttk.Button(btns, text="Delete", command=delete_row).pack(side="left", padx=6)
    ttk.Button(btns, text="Refresh", command=refresh).pack(side="left", padx=6)

    refresh()
    return frame, refresh
