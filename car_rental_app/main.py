import tkinter as tk
from tkinter import ttk

from car_rental_app.tabs import guests, hotels, invoices, rental_cars, reservations, rooms
from car_rental_app.tabs.common import setup_tree_style


def main():
    root = tk.Tk()
    setup_tree_style()
    root.title("Car Rental System")
    root.geometry("1100x720")
    root.minsize(900, 560)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=8)

    notebook.add(hotels.build(notebook), text="Branches")
    notebook.add(rooms.build(notebook), text="Cars")
    notebook.add(guests.build(notebook), text="Customers")
    notebook.add(reservations.build(notebook), text="Rentals")
    notebook.add(rental_cars.build(notebook), text="Rental Cars")
    notebook.add(invoices.build(notebook), text="Payments")

    root.mainloop()


if __name__ == "__main__":
    main()
