
import tkinter as tk
from tkinter import messagebox, ttk

from hotel_app.db import get_connection
from hotel_app.tabs.common import clear_tree, show_db_error


def build(parent) :
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(8, weight=1)

    ttk.Label(frame, text="Guests", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w")

    gid_var = tk.StringVar()
    ttk.Label(frame, text="Guest ID (auto)").grid(row=1, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=gid_var, width=12, state="readonly").grid(row=1, column=1, sticky="w")

    fn_var = tk.StringVar()
    ttk.Label(frame, text="First name *").grid(row=2, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=fn_var, width=32).grid(row=2, column=1, sticky="we")

    ln_var = tk.StringVar()
    ttk.Label(frame, text="Last name *").grid(row=3, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=ln_var, width=32).grid(row=3, column=1, sticky="we")

    email_var = tk.StringVar()
    ttk.Label(frame, text="Email *").grid(row=4, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=email_var, width=32).grid(row=4, column=1, sticky="we")

    phone_var = tk.StringVar()
    ttk.Label(frame, text="Phone *").grid(row=5, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=phone_var, width=32).grid(row=5, column=1, sticky="we")

    nation_var = tk.StringVar()
    ttk.Label(frame, text="Nationality *").grid(row=6, column=0, sticky="w", pady=2)
    ttk.Entry(frame, textvariable=nation_var, width=32).grid(row=6, column=1, sticky="we")

    search_var = tk.StringVar()
    ttk.Label(frame, text="Search by guest ID").grid(row=7, column=0, sticky="w", pady=(8, 2))
    ttk.Entry(frame, textvariable=search_var, width=14).grid(row=7, column=1, sticky="w")

    cols = ("guest_id", "first_name", "last_name", "email", "phone", "nationality")
    tree = ttk.Treeview(frame, columns=cols, show="headings", height=14)
    for c, w in zip(cols, (70, 100, 100, 200, 120, 100)):
        tree.heading(c, text=c.replace("_", " ").title())
        tree.column(c, anchor="w", width=w)
    tree.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=8)

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scroll.grid(row=8, column=3, sticky="ns", pady=8)
    tree.configure(yscrollcommand=scroll.set)

    def load_row(_e=None) :
        sel = tree.selection()
        if not sel:
            return
        v = tree.item(sel[0], "values")
        gid_var.set(str(v[0]))
        fn_var.set(v[1])
        ln_var.set(v[2])
        email_var.set(v[3])
        phone_var.set(v[4])
        nation_var.set(v[5])

    tree.bind("<<TreeviewSelect>>", load_row)

    def clear_form() :
        gid_var.set("")
        fn_var.set("")
        ln_var.set("")
        email_var.set("")
        phone_var.set("")
        nation_var.set("")

    def refresh() :
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                """
                SELECT guest_id, first_name, last_name, email, phone, nationality
                FROM guest
                ORDER BY guest_id
                """
            )
            rows = cur.fetchall()
            cn.close()
            clear_tree(tree)
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), values=r)
            clear_form()
        except Exception as exc:
            show_db_error(frame, exc)

    def search_id() :
        sid = search_var.get().strip()
        if not sid:
            refresh()
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                """
                SELECT guest_id, first_name, last_name, email, phone, nationality
                FROM guest WHERE guest_id=%s
                """,
                (int(sid),),
            )
            rows = cur.fetchall()
            cn.close()
            clear_tree(tree)
            for r in rows:
                tree.insert("", tk.END, iid=str(r[0]), values=r)
            if rows:
                tree.selection_set(str(rows[0][0]))
                load_row()
            else:
                messagebox.showinfo("Guests", "No guest with that ID.", parent=frame)
        except Exception as exc:
            show_db_error(frame, exc)

    def insert_guest() :
        try:
            if not email_var.get().strip() or not phone_var.get().strip():
                messagebox.showwarning("Guests", "Email and phone are required.", parent=frame)
                return
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                """
                INSERT INTO guest (first_name, last_name, email, phone, nationality)
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    fn_var.get().strip(),
                    ln_var.get().strip(),
                    email_var.get().strip(),
                    phone_var.get().strip(),
                    nation_var.get().strip(),
                ),
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Guests", "Guest inserted.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def update_guest() :
        try:
            if not gid_var.get().strip():
                messagebox.showwarning("Guests", "Select a guest to update.", parent=frame)
                return
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                """
                UPDATE guest SET first_name=%s, last_name=%s, email=%s, phone=%s, nationality=%s
                WHERE guest_id=%s
                """,
                (
                    fn_var.get().strip(),
                    ln_var.get().strip(),
                    email_var.get().strip(),
                    phone_var.get().strip(),
                    nation_var.get().strip(),
                    int(gid_var.get()),
                ),
            )
            cn.commit()
            cn.close()
            messagebox.showinfo("Guests", "Guest updated.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    def delete_guest() :
        if not gid_var.get().strip():
            messagebox.showwarning("Guests", "Select a guest to delete.", parent=frame)
            return
        if not messagebox.askyesno("Guests", "Delete this guest? (Fails if reservations exist.)", parent=frame):
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute("DELETE FROM guest WHERE guest_id=%s", (int(gid_var.get()),))
            cn.commit()
            cn.close()
            messagebox.showinfo("Guests", "Guest deleted.", parent=frame)
            refresh()
        except Exception as exc:
            show_db_error(frame, exc)

    btns = ttk.Frame(frame)
    btns.grid(row=9, column=0, columnspan=3, sticky="w")
    ttk.Button(btns, text="Insert", command=insert_guest).pack(side="left", padx=(0, 6))
    ttk.Button(btns, text="Update", command=update_guest).pack(side="left", padx=6)
    ttk.Button(btns, text="Delete", command=delete_guest).pack(side="left", padx=6)
    ttk.Button(btns, text="Refresh", command=refresh).pack(side="left", padx=6)
    ttk.Button(btns, text="Search", command=search_id).pack(side="left", padx=12)

    refresh()
    frame.bind('<Visibility>', lambda e: refresh())
    refresh()
    return frame
