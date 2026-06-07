import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import FIELD_PADY, SEARCH_PADY, clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(10, weight=1)

    ttk.Label(frame, text="Employees", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Employee ID").grid(row=1, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w", pady=FIELD_PADY)

    fn_var = tk.StringVar()
    ttk.Label(frame, text="First Name *").grid(row=2, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=fn_var, width=28).grid(row=2, column=1, sticky="w", pady=FIELD_PADY)

    ln_var = tk.StringVar()
    ttk.Label(frame, text="Last Name *").grid(row=3, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=ln_var, width=28).grid(row=3, column=1, sticky="w", pady=FIELD_PADY)

    role_var = tk.StringVar()
    ttk.Label(frame, text="Role *").grid(row=4, column=0, sticky="w", pady=FIELD_PADY)
    role_combo = ttk.Combobox(frame, textvariable=role_var, values=("Agent", "Mechanic", "Manager", "Sales", "Security", "Maintenance"), width=25, state="readonly")
    role_combo.grid(row=4, column=1, sticky="w", pady=FIELD_PADY)

    sal_var = tk.StringVar()
    ttk.Label(frame, text="Salary *").grid(row=5, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=sal_var, width=16).grid(row=5, column=1, sticky="w", pady=FIELD_PADY)

    hire_var = tk.StringVar()
    ttk.Label(frame, text="Hire Date (YYYY-MM-DD) *").grid(row=6, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=hire_var, width=16).grid(row=6, column=1, sticky="w", pady=FIELD_PADY)

    hotel_var = tk.StringVar()
    ttk.Label(frame, text="Branch *").grid(row=7, column=0, sticky="w", pady=FIELD_PADY)
    hotel_combo = ttk.Combobox(frame, textvariable=hotel_var, width=36, state="readonly")
    hotel_combo.grid(row=7, column=1, sticky="w", pady=FIELD_PADY)

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Name/ID)").grid(row=8, column=0, sticky="w", pady=SEARCH_PADY)
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=8, column=1, sticky="w", pady=SEARCH_PADY)

    cols = ("employee_id", "first_name", "last_name", "role", "salary", "hire_date", "branch_id")
    headings = ("Employee ID", "First Name", "Last Name", "Role", "Salary", "Hire Date", "Branch ID")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, h, w in zip(cols, headings, (80, 100, 100, 100, 80, 100, 80)):
        tree.heading(c, text=h)
        tree.column(c, width=w, anchor="w")
    tree.grid(row=10, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=10, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_combos():
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("SELECT branch_id, name FROM branch ORDER BY branch_id")
            rows = cur.fetchall()
            cn.close()
            vals = [f"{r[0]} | {r[1]}" for r in rows]
            hotel_combo["values"] = vals
        except Exception as exc:
            pass

    def get_combo_id(var_str):
        if not var_str.strip(): return None
        return int(var_str.split("|")[0].strip())

    def load_row(_e=None):
        sel = tree.selection()
        if not sel: return
        v = tree.item(sel[0], "values")
        id_var.set(str(v[0]))
        fn_var.set(v[1])
        ln_var.set(v[2])
        role_var.set(v[3])
        sal_var.set(str(v[4]))
        hire_var.set(str(v[5]))
        hid = str(v[6])
        for val in hotel_combo["values"]:
            if val.startswith(hid + " |"):
                hotel_combo.set(val)
                break

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        fn_var.set("")
        ln_var.set("")
        role_var.set("")
        sal_var.set("")
        hire_var.set("")
        hotel_var.set("")
        search_var.set("")

    def refresh(search=""):
        load_combos()
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search:
                if search.isdigit():
                    cur.execute("SELECT employee_id, first_name, last_name, role, salary, hire_date, branch_id FROM employee WHERE employee_id = %s", (int(search),))
                else:
                    cur.execute("SELECT employee_id, first_name, last_name, role, salary, hire_date, branch_id FROM employee WHERE first_name LIKE %s OR last_name LIKE %s", ('%'+search+'%', '%'+search+'%'))
            else:
                cur.execute("SELECT employee_id, first_name, last_name, role, salary, hire_date, branch_id FROM employee ORDER BY employee_id")
            rows = cur.fetchall()
            cn.close()
            clear_tree(tree)
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), values=r)
        except Exception as exc:
            show_db_error(frame, exc)

    def do_search():
        refresh(search_var.get().strip())

    def do_insert():
        hid = get_combo_id(hotel_var.get())
        if not id_var.get().strip() or not hid or not fn_var.get().strip() or not ln_var.get().strip() or not hire_var.get().strip() or not sal_var.get().strip() or not role_var.get().strip():
            messagebox.showwarning("Employees", "All fields are required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO employee (employee_id, first_name, last_name, role, salary, hire_date, branch_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (int(id_var.get()), fn_var.get().strip(), ln_var.get().strip(), role_var.get(), float(sal_var.get()), hire_var.get(), hid)
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Employees", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Employees", "Select a record.", parent=frame)
            return
        hid = get_combo_id(hotel_var.get())
        if not hid or not fn_var.get().strip() or not ln_var.get().strip() or not hire_var.get().strip() or not sal_var.get().strip() or not role_var.get().strip():
            messagebox.showwarning("Employees", "All fields are required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE employee SET first_name=%s, last_name=%s, role=%s, salary=%s, hire_date=%s, branch_id=%s WHERE employee_id=%s",
                (fn_var.get().strip(), ln_var.get().strip(), role_var.get(), float(sal_var.get()), hire_var.get(), hid, int(id_var.get()))
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Employees", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Employees", "Select a record.", parent=frame)
            return
        if not messagebox.askyesno("Employees", "Delete this record?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM employee WHERE employee_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Employees", "Deleted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=11, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind('<Visibility>', lambda e: refresh())
    return frame
