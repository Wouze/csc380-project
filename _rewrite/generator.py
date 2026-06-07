import os

tabs_dir = '../car_rental_app/tabs'

# 1. hotels.py
with open(f'{tabs_dir}/hotels.py', 'w') as f:
    f.write('''import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(8, weight=1)

    ttk.Label(frame, text="Hotels", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Hotel ID").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    name_var = tk.StringVar()
    ttk.Label(frame, text="Name *").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame, textvariable=name_var, width=32).grid(row=2, column=1, sticky="w")

    addr_var = tk.StringVar()
    ttk.Label(frame, text="Address *").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=addr_var, width=32).grid(row=3, column=1, sticky="w")

    phone_var = tk.StringVar()
    ttk.Label(frame, text="Phone").grid(row=4, column=0, sticky="w")
    ttk.Entry(frame, textvariable=phone_var, width=32).grid(row=4, column=1, sticky="w")

    email_var = tk.StringVar()
    ttk.Label(frame, text="Email").grid(row=5, column=0, sticky="w")
    ttk.Entry(frame, textvariable=email_var, width=32).grid(row=5, column=1, sticky="w")

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Name or ID)").grid(row=6, column=0, sticky="w", pady=(8,2))
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=6, column=1, sticky="w", pady=(8,2))

    cols = ("hotel_id", "name", "address", "phone", "email")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (60, 150, 200, 100, 150)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=8, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_row(_e=None):
        sel = tree.selection()
        if not sel: return
        v = tree.item(sel[0], "values")
        id_var.set(str(v[0]))
        name_var.set(v[1])
        addr_var.set(v[2])
        phone_var.set(v[3])
        email_var.set(v[4])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        name_var.set("")
        addr_var.set("")
        phone_var.set("")
        email_var.set("")
        search_var.set("")

    def refresh(search=""):
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search:
                if search.isdigit():
                    cur.execute("SELECT hotel_id, name, address, phone, email FROM hotel WHERE hotel_id = %s", (int(search),))
                else:
                    cur.execute("SELECT hotel_id, name, address, phone, email FROM hotel WHERE name ILIKE %s", ('%'+search+'%',))
            else:
                cur.execute("SELECT hotel_id, name, address, phone, email FROM hotel ORDER BY hotel_id")
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
        if not name_var.get().strip() or not addr_var.get().strip():
            messagebox.showwarning("Hotels", "Name and Address are required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO hotel (name, address, phone, email) VALUES (%s,%s,%s,%s)",
                (name_var.get().strip(), addr_var.get().strip(), phone_var.get().strip(), email_var.get().strip())
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Hotels", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Hotels", "Select a record.", parent=frame)
            return
        if not name_var.get().strip() or not addr_var.get().strip():
            messagebox.showwarning("Hotels", "Name and Address are required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE hotel SET name=%s, address=%s, phone=%s, email=%s WHERE hotel_id=%s",
                (name_var.get().strip(), addr_var.get().strip(), phone_var.get().strip(), email_var.get().strip(), int(id_var.get()))
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Hotels", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Hotels", "Select a record.", parent=frame)
            return
        if not messagebox.askyesno("Hotels", "Delete this record?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM hotel WHERE hotel_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Hotels", "Deleted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=9, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind('<Visibility>', lambda e: refresh())
    return frame
''')

# 2. guests.py
with open(f'{tabs_dir}/guests.py', 'w') as f:
    f.write('''import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(9, weight=1)

    ttk.Label(frame, text="Guests", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Guest ID").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    fn_var = tk.StringVar()
    ttk.Label(frame, text="First Name *").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame, textvariable=fn_var, width=32).grid(row=2, column=1, sticky="w")

    ln_var = tk.StringVar()
    ttk.Label(frame, text="Last Name *").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=ln_var, width=32).grid(row=3, column=1, sticky="w")

    email_var = tk.StringVar()
    ttk.Label(frame, text="Email *").grid(row=4, column=0, sticky="w")
    ttk.Entry(frame, textvariable=email_var, width=32).grid(row=4, column=1, sticky="w")

    phone_var = tk.StringVar()
    ttk.Label(frame, text="Phone *").grid(row=5, column=0, sticky="w")
    ttk.Entry(frame, textvariable=phone_var, width=32).grid(row=5, column=1, sticky="w")

    nat_var = tk.StringVar()
    ttk.Label(frame, text="Nationality *").grid(row=6, column=0, sticky="w")
    ttk.Entry(frame, textvariable=nat_var, width=32).grid(row=6, column=1, sticky="w")

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Name/ID)").grid(row=7, column=0, sticky="w", pady=(8,2))
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=7, column=1, sticky="w", pady=(8,2))

    cols = ("guest_id", "first_name", "last_name", "email", "phone", "nationality")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (60, 100, 100, 150, 100, 100)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=9, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=9, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_row(_e=None):
        sel = tree.selection()
        if not sel: return
        v = tree.item(sel[0], "values")
        id_var.set(str(v[0]))
        fn_var.set(v[1])
        ln_var.set(v[2])
        email_var.set(v[3])
        phone_var.set(v[4])
        nat_var.set(v[5])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        fn_var.set("")
        ln_var.set("")
        email_var.set("")
        phone_var.set("")
        nat_var.set("")
        search_var.set("")

    def refresh(search=""):
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search:
                if search.isdigit():
                    cur.execute("SELECT guest_id, first_name, last_name, email, phone, nationality FROM guest WHERE guest_id = %s", (int(search),))
                else:
                    cur.execute("SELECT guest_id, first_name, last_name, email, phone, nationality FROM guest WHERE first_name ILIKE %s OR last_name ILIKE %s", ('%'+search+'%', '%'+search+'%'))
            else:
                cur.execute("SELECT guest_id, first_name, last_name, email, phone, nationality FROM guest ORDER BY guest_id")
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
        if not fn_var.get().strip() or not ln_var.get().strip() or not email_var.get().strip() or not phone_var.get().strip() or not nat_var.get().strip():
            messagebox.showwarning("Guests", "All * fields required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO guest (first_name, last_name, email, phone, nationality) VALUES (%s,%s,%s,%s,%s)",
                (fn_var.get().strip(), ln_var.get().strip(), email_var.get().strip(), phone_var.get().strip(), nat_var.get().strip())
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Guests", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Guests", "Select a record.", parent=frame)
            return
        if not fn_var.get().strip() or not ln_var.get().strip() or not email_var.get().strip() or not phone_var.get().strip() or not nat_var.get().strip():
            messagebox.showwarning("Guests", "All * fields required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE guest SET first_name=%s, last_name=%s, email=%s, phone=%s, nationality=%s WHERE guest_id=%s",
                (fn_var.get().strip(), ln_var.get().strip(), email_var.get().strip(), phone_var.get().strip(), nat_var.get().strip(), int(id_var.get()))
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Guests", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Guests", "Select a record.", parent=frame)
            return
        if not messagebox.askyesno("Guests", "Delete this record?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM guest WHERE guest_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Guests", "Deleted successfully.", parent=frame)
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
''')

# 3. employees.py
with open(f'{tabs_dir}/employees.py', 'w') as f:
    f.write('''import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(10, weight=1)

    ttk.Label(frame, text="Employees", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Employee ID").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    fn_var = tk.StringVar()
    ttk.Label(frame, text="First Name *").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame, textvariable=fn_var, width=28).grid(row=2, column=1, sticky="w")

    ln_var = tk.StringVar()
    ttk.Label(frame, text="Last Name *").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=ln_var, width=28).grid(row=3, column=1, sticky="w")

    role_var = tk.StringVar()
    ttk.Label(frame, text="Role *").grid(row=4, column=0, sticky="w")
    role_combo = ttk.Combobox(frame, textvariable=role_var, values=("Receptionist", "Housekeeper", "Manager", "Chef", "Security", "Maintenance"), width=25, state="readonly")
    role_combo.grid(row=4, column=1, sticky="w")

    sal_var = tk.StringVar()
    ttk.Label(frame, text="Salary *").grid(row=5, column=0, sticky="w")
    ttk.Entry(frame, textvariable=sal_var, width=16).grid(row=5, column=1, sticky="w")

    hire_var = tk.StringVar()
    ttk.Label(frame, text="Hire Date (YYYY-MM-DD) *").grid(row=6, column=0, sticky="w")
    ttk.Entry(frame, textvariable=hire_var, width=16).grid(row=6, column=1, sticky="w")

    hotel_var = tk.StringVar()
    ttk.Label(frame, text="Hotel *").grid(row=7, column=0, sticky="w")
    hotel_combo = ttk.Combobox(frame, textvariable=hotel_var, width=36, state="readonly")
    hotel_combo.grid(row=7, column=1, sticky="w")

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Name/ID)").grid(row=8, column=0, sticky="w", pady=(8,2))
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=8, column=1, sticky="w", pady=(8,2))

    cols = ("employee_id", "first_name", "last_name", "role", "salary", "hire_date", "hotel_id")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (80, 100, 100, 100, 80, 100, 80)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=10, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=10, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_combos():
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("SELECT hotel_id, name FROM hotel ORDER BY hotel_id")
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
                    cur.execute("SELECT employee_id, first_name, last_name, role, salary, hire_date, hotel_id FROM employee WHERE employee_id = %s", (int(search),))
                else:
                    cur.execute("SELECT employee_id, first_name, last_name, role, salary, hire_date, hotel_id FROM employee WHERE first_name ILIKE %s OR last_name ILIKE %s", ('%'+search+'%', '%'+search+'%'))
            else:
                cur.execute("SELECT employee_id, first_name, last_name, role, salary, hire_date, hotel_id FROM employee ORDER BY employee_id")
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
        if not hid or not fn_var.get().strip() or not ln_var.get().strip() or not hire_var.get().strip() or not sal_var.get().strip() or not role_var.get().strip():
            messagebox.showwarning("Employees", "All fields are required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO employee (first_name, last_name, role, salary, hire_date, hotel_id) VALUES (%s,%s,%s,%s,%s,%s)",
                (fn_var.get().strip(), ln_var.get().strip(), role_var.get(), float(sal_var.get()), hire_var.get(), hid)
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
                "UPDATE employee SET first_name=%s, last_name=%s, role=%s, salary=%s, hire_date=%s, hotel_id=%s WHERE employee_id=%s",
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
''')

# 4. rooms.py
with open(f'{tabs_dir}/rooms.py', 'w') as f:
    f.write('''import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(11, weight=1)

    ttk.Label(frame, text="Rooms", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Room ID").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    hotel_var = tk.StringVar()
    ttk.Label(frame, text="Hotel *").grid(row=2, column=0, sticky="w")
    hotel_combo = ttk.Combobox(frame, textvariable=hotel_var, width=36, state="readonly")
    hotel_combo.grid(row=2, column=1, sticky="w")

    room_num_var = tk.StringVar()
    ttk.Label(frame, text="Room Number *").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=room_num_var, width=16).grid(row=3, column=1, sticky="w")

    floor_var = tk.StringVar()
    ttk.Label(frame, text="Floor *").grid(row=4, column=0, sticky="w")
    ttk.Entry(frame, textvariable=floor_var, width=16).grid(row=4, column=1, sticky="w")

    type_var = tk.StringVar()
    ttk.Label(frame, text="Room Type *").grid(row=5, column=0, sticky="w")
    ttk.Combobox(frame, textvariable=type_var, values=("Single", "Double", "Suite"), width=16, state="readonly").grid(row=5, column=1, sticky="w")

    price_var = tk.StringVar()
    ttk.Label(frame, text="Price per Night *").grid(row=6, column=0, sticky="w")
    ttk.Entry(frame, textvariable=price_var, width=16).grid(row=6, column=1, sticky="w")

    cap_var = tk.StringVar()
    ttk.Label(frame, text="Max Capacity *").grid(row=7, column=0, sticky="w")
    ttk.Entry(frame, textvariable=cap_var, width=16).grid(row=7, column=1, sticky="w")

    status_var = tk.StringVar()
    ttk.Label(frame, text="Status *").grid(row=8, column=0, sticky="w")
    ttk.Combobox(frame, textvariable=status_var, values=("Available", "Occupied", "Maintenance"), width=16, state="readonly").grid(row=8, column=1, sticky="w")

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Room ID)").grid(row=9, column=0, sticky="w", pady=(8,2))
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=9, column=1, sticky="w", pady=(8,2))

    cols = ("room_id", "hotel_id", "room_number", "floor", "room_type", "price_per_night", "max_capacity", "status")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (60, 60, 90, 50, 80, 90, 80, 80)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=11, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=11, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_combos():
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("SELECT hotel_id, name FROM hotel ORDER BY hotel_id")
            rows = cur.fetchall()
            cn.close()
            hotel_combo["values"] = [f"{r[0]} | {r[1]}" for r in rows]
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
        hid = str(v[1])
        for val in hotel_combo["values"]:
            if val.startswith(hid + " |"):
                hotel_combo.set(val)
                break
        room_num_var.set(v[2])
        floor_var.set(str(v[3]))
        type_var.set(v[4])
        price_var.set(str(v[5]))
        cap_var.set(str(v[6]))
        status_var.set(v[7])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        hotel_var.set("")
        room_num_var.set("")
        floor_var.set("")
        type_var.set("")
        price_var.set("")
        cap_var.set("")
        status_var.set("")
        search_var.set("")

    def refresh(search=""):
        load_combos()
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search and search.isdigit():
                cur.execute("SELECT room_id, hotel_id, room_number, floor, room_type, price_per_night, max_capacity, status FROM room WHERE room_id = %s", (int(search),))
            else:
                cur.execute("SELECT room_id, hotel_id, room_number, floor, room_type, price_per_night, max_capacity, status FROM room ORDER BY room_id")
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
        if not hid or not room_num_var.get().strip() or not price_var.get().strip():
            messagebox.showwarning("Rooms", "Required fields missing.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO room (hotel_id, room_number, floor, room_type, price_per_night, max_capacity, status) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (hid, room_num_var.get().strip(), int(floor_var.get()), type_var.get(), float(price_var.get()), int(cap_var.get()), status_var.get())
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Rooms", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Rooms", "Select a room.", parent=frame)
            return
        hid = get_combo_id(hotel_var.get())
        if not hid or not room_num_var.get().strip() or not price_var.get().strip():
            messagebox.showwarning("Rooms", "Required fields missing.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE room SET hotel_id=%s, room_number=%s, floor=%s, room_type=%s, price_per_night=%s, max_capacity=%s, status=%s WHERE room_id=%s",
                (hid, room_num_var.get().strip(), int(floor_var.get()), type_var.get(), float(price_var.get()), int(cap_var.get()), status_var.get(), int(id_var.get()))
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Rooms", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Rooms", "Select a room.", parent=frame)
            return
        if not messagebox.askyesno("Rooms", "Delete this room?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM room WHERE room_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Rooms", "Deleted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=12, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind('<Visibility>', lambda e: refresh())
    return frame
''')

# 5. reservations.py
with open(f'{tabs_dir}/reservations.py', 'w') as f:
    f.write('''import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(9, weight=1)

    ttk.Label(frame, text="Reservations", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Reservation ID").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    guest_var = tk.StringVar()
    ttk.Label(frame, text="Guest *").grid(row=2, column=0, sticky="w")
    guest_combo = ttk.Combobox(frame, textvariable=guest_var, width=36, state="readonly")
    guest_combo.grid(row=2, column=1, sticky="w")

    booking_var = tk.StringVar()
    ttk.Label(frame, text="Booking Date *").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=booking_var, width=16).grid(row=3, column=1, sticky="w")
    ttk.Label(frame, text="(YYYY-MM-DD)", foreground="gray").grid(row=3, column=2, sticky="w")

    in_var = tk.StringVar()
    ttk.Label(frame, text="Check-in *").grid(row=4, column=0, sticky="w")
    ttk.Entry(frame, textvariable=in_var, width=16).grid(row=4, column=1, sticky="w")

    out_var = tk.StringVar()
    ttk.Label(frame, text="Check-out *").grid(row=5, column=0, sticky="w")
    ttk.Entry(frame, textvariable=out_var, width=16).grid(row=5, column=1, sticky="w")

    status_var = tk.StringVar()
    ttk.Label(frame, text="Status *").grid(row=6, column=0, sticky="w")
    ttk.Combobox(frame, textvariable=status_var, values=("confirmed", "checked-in", "checked-out", "cancelled"), width=16, state="readonly").grid(row=6, column=1, sticky="w")

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Reservation ID)").grid(row=7, column=0, sticky="w", pady=(8,2))
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=7, column=1, sticky="w", pady=(8,2))

    cols = ("reservation_id", "guest_id", "booking_date", "check_in_date", "check_out_date", "status")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (90, 60, 100, 100, 100, 100)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=9, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=9, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_combos():
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("SELECT guest_id, first_name, last_name FROM guest ORDER BY guest_id")
            rows = cur.fetchall()
            cn.close()
            guest_combo["values"] = [f"{r[0]} | {r[1]} {r[2]}" for r in rows]
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
        gid = str(v[1])
        for val in guest_combo["values"]:
            if val.startswith(gid + " |"):
                guest_combo.set(val)
                break
        booking_var.set(v[2])
        in_var.set(v[3])
        out_var.set(v[4])
        status_var.set(v[5])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        guest_var.set("")
        booking_var.set("")
        in_var.set("")
        out_var.set("")
        status_var.set("")
        search_var.set("")

    def refresh(search=""):
        load_combos()
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search and search.isdigit():
                cur.execute("SELECT reservation_id, guest_id, booking_date, check_in_date, check_out_date, status FROM reservation WHERE reservation_id = %s", (int(search),))
            else:
                cur.execute("SELECT reservation_id, guest_id, booking_date, check_in_date, check_out_date, status FROM reservation ORDER BY reservation_id")
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
        gid = get_combo_id(guest_var.get())
        if not gid or not booking_var.get().strip() or not in_var.get().strip() or not out_var.get().strip():
            messagebox.showwarning("Reservations", "Required fields missing.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO reservation (guest_id, booking_date, check_in_date, check_out_date, status) VALUES (%s,%s,%s,%s,%s)",
                (gid, booking_var.get().strip(), in_var.get().strip(), out_var.get().strip(), status_var.get())
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Reservations", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Reservations", "Select a record.", parent=frame)
            return
        gid = get_combo_id(guest_var.get())
        if not gid or not booking_var.get().strip() or not in_var.get().strip() or not out_var.get().strip():
            messagebox.showwarning("Reservations", "Required fields missing.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE reservation SET guest_id=%s, booking_date=%s, check_in_date=%s, check_out_date=%s, status=%s WHERE reservation_id=%s",
                (gid, booking_var.get().strip(), in_var.get().strip(), out_var.get().strip(), status_var.get(), int(id_var.get()))
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Reservations", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Reservations", "Select a record.", parent=frame)
            return
        if not messagebox.askyesno("Reservations", "Delete this reservation?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM reservation WHERE reservation_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Reservations", "Deleted successfully.", parent=frame)
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
''')

# 6. invoices.py
with open(f'{tabs_dir}/invoices.py', 'w') as f:
    f.write('''import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(8, weight=1)

    ttk.Label(frame, text="Invoices", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Invoice ID").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=id_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    res_var = tk.StringVar()
    ttk.Label(frame, text="Reservation *").grid(row=2, column=0, sticky="w")
    res_combo = ttk.Combobox(frame, textvariable=res_var, width=36, state="readonly")
    res_combo.grid(row=2, column=1, sticky="w")

    amt_var = tk.StringVar()
    ttk.Label(frame, text="Total Amount *").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=amt_var, width=16).grid(row=3, column=1, sticky="w")

    date_var = tk.StringVar()
    ttk.Label(frame, text="Issue Date *").grid(row=4, column=0, sticky="w")
    ttk.Entry(frame, textvariable=date_var, width=16).grid(row=4, column=1, sticky="w")
    ttk.Label(frame, text="(YYYY-MM-DD)", foreground="gray").grid(row=4, column=2, sticky="w")

    paid_var = tk.StringVar()
    ttk.Label(frame, text="Is Paid?").grid(row=5, column=0, sticky="w")
    ttk.Combobox(frame, textvariable=paid_var, values=("Yes", "No"), width=16, state="readonly").grid(row=5, column=1, sticky="w")

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Invoice ID)").grid(row=6, column=0, sticky="w", pady=(8,2))
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=6, column=1, sticky="w", pady=(8,2))

    cols = ("invoice_id", "reservation_id", "total_amount", "issue_date", "is_paid")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
    for c, w in zip(cols, (80, 100, 100, 120, 80)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, width=w, anchor="w")
    tree.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=8, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_combos():
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("SELECT reservation_id FROM reservation ORDER BY reservation_id")
            rows = cur.fetchall()
            cn.close()
            res_combo["values"] = [f"{r[0]} | Reservation {r[0]}" for r in rows]
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
        date_var.set(v[3])
        paid_var.set("Yes" if v[4] in [True, "True", 1, "1", "Yes", "yes"] else "No")

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        res_var.set("")
        amt_var.set("")
        date_var.set("")
        paid_var.set("")
        search_var.set("")

    def refresh(search=""):
        load_combos()
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search and search.isdigit():
                cur.execute("SELECT invoice_id, reservation_id, total_amount, issue_date, is_paid FROM invoice WHERE invoice_id = %s", (int(search),))
            else:
                cur.execute("SELECT invoice_id, reservation_id, total_amount, issue_date, is_paid FROM invoice ORDER BY invoice_id")
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
        rid = get_combo_id(res_var.get())
        if not rid or not amt_var.get().strip() or not date_var.get().strip():
            messagebox.showwarning("Invoices", "Required fields missing.", parent=frame)
            return
        is_paid = paid_var.get() == "Yes"
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO invoice (reservation_id, total_amount, issue_date, is_paid) VALUES (%s,%s,%s,%s)",
                (rid, float(amt_var.get().strip()), date_var.get().strip(), is_paid)
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Invoices", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Invoices", "Select a record.", parent=frame)
            return
        rid = get_combo_id(res_var.get())
        if not rid or not amt_var.get().strip() or not date_var.get().strip():
            messagebox.showwarning("Invoices", "Required fields missing.", parent=frame)
            return
        is_paid = paid_var.get() == "Yes"
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE invoice SET reservation_id=%s, total_amount=%s, issue_date=%s, is_paid=%s WHERE invoice_id=%s",
                (rid, float(amt_var.get().strip()), date_var.get().strip(), is_paid, int(id_var.get()))
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Invoices", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Invoices", "Select a record.", parent=frame)
            return
        if not messagebox.askyesno("Invoices", "Delete this invoice?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM invoice WHERE invoice_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Invoices", "Deleted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=9, column=0, columnspan=3, sticky="w")
    ttk.Button(btn_frame, text="Insert", command=do_insert).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Update", command=do_update).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Delete", command=do_delete).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Search", command=do_search).pack(side="left", padx=2)
    ttk.Button(btn_frame, text="Clear", command=lambda: [clear(), refresh()]).pack(side="left", padx=2)

    refresh()
    frame.bind('<Visibility>', lambda e: refresh())
    return frame
''')
