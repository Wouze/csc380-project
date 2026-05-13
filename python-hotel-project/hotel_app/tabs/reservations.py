import tkinter as tk
from tkinter import messagebox, ttk
from hotel_app.db import get_connection
from hotel_app.tabs.common import clear_tree, show_db_error

def build(parent):
    frame = ttk.Frame(parent, padding=8)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(9, weight=1)

    ttk.Label(frame, text="Reservations", font=("", 14, "bold")).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,8))

    id_var = tk.StringVar()
    ttk.Label(frame, text="Reservation ID").grid(row=1, column=0, sticky="w")
    ttk.Entry(frame, textvariable=id_var, width=12).grid(row=1, column=1, sticky="w")

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
            if search:
                if search.isdigit():
                    cur.execute("SELECT reservation_id, guest_id, booking_date, check_in_date, check_out_date, status FROM reservation WHERE reservation_id = %s", (int(search),))
                else:
                    cur.execute("SELECT reservation_id, guest_id, booking_date, check_in_date, check_out_date, status FROM reservation WHERE status LIKE %s", ("%" + search + "%",))
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
        if not id_var.get().strip() or not gid or not booking_var.get().strip() or not in_var.get().strip() or not out_var.get().strip() or not status_var.get().strip():
            messagebox.showwarning("Reservations", "Required fields missing.", parent=frame)
            return
        try:
            cn = get_connection()
            cur = cn.cursor()
            cur.execute(
                "INSERT INTO reservation (reservation_id, guest_id, booking_date, check_in_date, check_out_date, status) VALUES (%s,%s,%s,%s,%s,%s)",
                (int(id_var.get()), gid, booking_var.get().strip(), in_var.get().strip(), out_var.get().strip(), status_var.get())
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
        if not gid or not booking_var.get().strip() or not in_var.get().strip() or not out_var.get().strip() or not status_var.get().strip():
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
