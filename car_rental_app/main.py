import tkinter as tk
from tkinter import messagebox, ttk

from car_rental_app.tabs import employees, guests, hotels, invoices, reservations, rooms


def main():
    root = tk.Tk()
    root.title("Car Rental System")
    root.geometry("1100x720")
    root.minsize(900, 560)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    notebook.add(hotels.build(notebook), text="Branches")
    notebook.add(rooms.build(notebook), text="Cars")
    notebook.add(guests.build(notebook), text="Customers")
    notebook.add(reservations.build(notebook), text="Rentals")
    notebook.add(invoices.build(notebook), text="Payments")
    notebook.add(employees.build(notebook), text="Employees")

    root.mainloop()


if __name__ == "__main__":
    main()
