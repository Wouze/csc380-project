import tkinter as tk
from tkinter import messagebox, ttk
from car_rental_app.db import get_connection
from car_rental_app.tabs.common import FIELD_PADY, SEARCH_PADY, create_tree_panel, fill_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(9, weight=1)

    ttk.Label(frame, text="Customers", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Customer ID").grid(row=1, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w", pady=FIELD_PADY)

    fn_var = tk.StringVar()
    ttk.Label(frame, text="First Name *").grid(row=2, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=fn_var, width=32).grid(row=2, column=1, sticky="w", pady=FIELD_PADY)

    ln_var = tk.StringVar()
    ttk.Label(frame, text="Last Name *").grid(row=3, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=ln_var, width=32).grid(row=3, column=1, sticky="w", pady=FIELD_PADY)

    email_var = tk.StringVar()
    ttk.Label(frame, text="Email *").grid(row=4, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=email_var, width=32).grid(row=4, column=1, sticky="w", pady=FIELD_PADY)

    phone_var = tk.StringVar()
    ttk.Label(frame, text="Phone *").grid(row=5, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=phone_var, width=32).grid(row=5, column=1, sticky="w", pady=FIELD_PADY)

    nat_var = tk.StringVar()
    ttk.Label(frame, text="Nationality *").grid(row=6, column=0, sticky="w", pady=FIELD_PADY)
    ttk.Entry(frame, textvariable=nat_var, width=32).grid(row=6, column=1, sticky="w", pady=FIELD_PADY)

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Name/ID)").grid(row=7, column=0, sticky="w", pady=SEARCH_PADY)
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=7, column=1, sticky="w", pady=SEARCH_PADY)

    cols = ("customer_id", "first_name", "last_name", "email", "phone", "nationality")
    headings = ("Customer ID", "First Name", "Last Name", "Email", "Phone", "Nationality")
    tree = create_tree_panel(frame, 9, cols, headings, (80, 100, 100, 150, 100, 100))

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
                    cur.execute("SELECT customer_id, first_name, last_name, email, phone, nationality FROM customer WHERE customer_id = %s", (int(search),))
                else:
                    cur.execute("SELECT customer_id, first_name, last_name, email, phone, nationality FROM customer WHERE first_name LIKE %s OR last_name LIKE %s", ('%'+search+'%', '%'+search+'%'))
            else:
                cur.execute("SELECT customer_id, first_name, last_name, email, phone, nationality FROM customer ORDER BY customer_id")
            rows = cur.fetchall()
            cn.close()
            fill_tree(tree, rows)
        except Exception as exc:
            show_db_error(frame, exc)

    def do_search():
        refresh(search_var.get().strip())

    def do_insert():
        if not id_var.get().strip() or not fn_var.get().strip() or not ln_var.get().strip() or not email_var.get().strip() or not phone_var.get().strip() or not nat_var.get().strip():
            messagebox.showwarning("Customers", "All * fields required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO customer (customer_id, first_name, last_name, email, phone, nationality) VALUES (%s,%s,%s,%s,%s,%s)",
                (int(id_var.get()), fn_var.get().strip(), ln_var.get().strip(), email_var.get().strip(), phone_var.get().strip(), nat_var.get().strip())
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Customers", "Inserted successfully.", parent=frame)
            clear()
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_update():
        if not id_var.get():
            messagebox.showwarning("Customers", "Select a record.", parent=frame)
            return
        if not fn_var.get().strip() or not ln_var.get().strip() or not email_var.get().strip() or not phone_var.get().strip() or not nat_var.get().strip():
            messagebox.showwarning("Customers", "All * fields required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE customer SET first_name=%s, last_name=%s, email=%s, phone=%s, nationality=%s WHERE customer_id=%s",
                (fn_var.get().strip(), ln_var.get().strip(), email_var.get().strip(), phone_var.get().strip(), nat_var.get().strip(), int(id_var.get()))
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Customers", "Updated successfully.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def do_delete():
        if not id_var.get():
            messagebox.showwarning("Customers", "Select a record.", parent=frame)
            return
        if not messagebox.askyesno("Customers", "Delete this record?", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM customer WHERE customer_id=%s", (int(id_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Customers", "Deleted successfully.", parent=frame)
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
