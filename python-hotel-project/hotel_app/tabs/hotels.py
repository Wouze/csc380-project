import tkinter as tk
from tkinter import messagebox, ttk
from hotel_app.db import get_connection
from hotel_app.tabs.common import clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(8, weight=1)

    ttk.Label(frame, text="Hotels", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Hotel ID *").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w")

    name_var = tk.StringVar()
    ttk.Label(frame, text="Name *").grid(row=2, column=0, sticky="w")
    ttk.Entry(frame, textvariable=name_var, width=32).grid(row=2, column=1, sticky="w")

    addr_var = tk.StringVar()
    ttk.Label(frame, text="Address *").grid(row=3, column=0, sticky="w")
    ttk.Entry(frame, textvariable=addr_var, width=32).grid(row=3, column=1, sticky="w")

    city_var = tk.StringVar()
    ttk.Label(frame, text="City *").grid(row=4, column=0, sticky="w")
    ttk.Entry(frame, textvariable=city_var, width=32).grid(row=4, column=1, sticky="w")

    phone_var = tk.StringVar()
    ttk.Label(frame, text="Phone *").grid(row=5, column=0, sticky="w")
    ttk.Entry(frame, textvariable=phone_var, width=32).grid(row=5, column=1, sticky="w")

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search (Name or ID)").grid(row=6, column=0, sticky="w", pady=(8,2))
    ttk.Entry(frame, textvariable=search_var, width=20).grid(row=6, column=1, sticky="w", pady=(8,2))

    cols = ("hotel_id", "name", "address", "city", "phone")
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
        city_var.set(v[3])
        phone_var.set(v[4])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear():
        id_var.set("")
        name_var.set("")
        addr_var.set("")
        city_var.set("")
        phone_var.set("")
        search_var.set("")

    def refresh(search=""):
        try:
            cn = get_connection()
            cur = cn.cursor()
            if search:
                if search.isdigit():
                    cur.execute("SELECT hotel_id, name, address, city, phone FROM hotel WHERE hotel_id = %s", (int(search),))
                else:
                    cur.execute("SELECT hotel_id, name, address, city, phone FROM hotel WHERE name LIKE %s", ('%'+search+'%',))
            else:
                cur.execute("SELECT hotel_id, name, address, city, phone FROM hotel ORDER BY hotel_id")
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
        if not id_var.get().strip() or not name_var.get().strip() or not addr_var.get().strip() or not city_var.get().strip() or not phone_var.get().strip():
            messagebox.showwarning("Hotels", "All * fields are required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO hotel (hotel_id, name, address, city, phone) VALUES (%s,%s,%s,%s,%s)",
                (int(id_var.get()), name_var.get().strip(), addr_var.get().strip(), city_var.get().strip(), phone_var.get().strip())
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
        if not id_var.get().strip() or not name_var.get().strip() or not addr_var.get().strip() or not city_var.get().strip() or not phone_var.get().strip():
            messagebox.showwarning("Hotels", "All * fields are required.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "UPDATE hotel SET name=%s, address=%s, city=%s, phone=%s WHERE hotel_id=%s",
                (name_var.get().strip(), addr_var.get().strip(), city_var.get().strip(), phone_var.get().strip(), int(id_var.get()))
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
