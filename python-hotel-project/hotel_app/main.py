import tkinter as tk
from tkinter import messagebox, ttk

from hotel_app.tabs import employees, guests, hotels, invoices, reservations, rooms

def main():
    root = tk.Tk()
    root.title("Hotel Management System")
    root.geometry("1100x720")
    root.minsize(900, 560)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    # Simplified tab creation
    notebook.add(hotels.build(notebook), text="Hotels")
    notebook.add(rooms.build(notebook), text="Rooms")
    notebook.add(guests.build(notebook), text="Guests")
    notebook.add(reservations.build(notebook), text="Reservations")
    notebook.add(invoices.build(notebook), text="Invoices")
    notebook.add(employees.build(notebook), text="Employees")

    root.mainloop()

if __name__ == "__main__":
    main()

