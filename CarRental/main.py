import tkinter as tk
from tkinter import messagebox
from typing import List
import csv
import os

# Car class to represent car information
class Car:
    def __init__(self, plate: str, make: str, model: str, year: int, mileage: int, rented: bool = False):
        self.plate = plate
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.rented = rented

# Inventory class to manage car inventory
class Inventory:
    def __init__(self):
        self.cars: List[Car] = []

    def add_car(self, car: Car) -> str:
        if any(existing_car.plate == car.plate for existing_car in self.cars):
            return "License plate already exists."
        self.cars.append(car)
        return "Car added successfully."

    def remove_car(self, plate: str) -> str:
        for car in self.cars:
            if car.plate == plate:
                self.cars.remove(car)
                return "Car removed successfully."
        return "Car not found."

    def find_car(self, plate: str) -> Car | None:
        return next((car for car in self.cars if car.plate == plate), None)

    def rent_car(self, plate: str) -> str:
        car = self.find_car(plate)
        if car:
            if car.rented:
                return "Car is already rented."
            car.rented = True
            return "Car rented successfully."
        return "Car not found."

    def return_car(self, plate: str) -> str:
        car = self.find_car(plate)
        if car:
            if not car.rented:
                return "Car is not currently rented."
            car.rented = False
            return "Car returned successfully."
        return "Car not found."

    def save_to_database(self, filename: str) -> None:
        saved_plates = set()
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    saved_plates.add(row['Plate'])

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Plate', 'Make', 'Model', 'Year', 'Mileage', 'Rented'])
            for car in self.cars:
                writer.writerow([car.plate, car.make, car.model, car.year, car.mileage, car.rented])

    def load_from_database(self, filename: str) -> None:
        self.cars.clear()
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    car = Car(row['Plate'], row['Make'], row['Model'], int(row['Year']), int(row['Mileage']), row['Rented'] == 'True')
                    self.cars.append(car)
        except FileNotFoundError:
            messagebox.showerror("Error", f"{filename} not found.")

# Tkinter-based GUI for the car inventory system
class InventoryGUI:
    def __init__(self, root):
        self.inventory = Inventory()
        self.root = root
        self.root.title("Car Rental System")
        self.root.configure(bg="#2d3142")

        # Load images
        self.add_image = tk.PhotoImage(file="Add Car.png")
        self.remove_image = tk.PhotoImage(file="Remove Car.png")
        self.find_image = tk.PhotoImage(file="Find Car.png")
        self.rent_image = tk.PhotoImage(file="Rent Car.png")
        self.return_image = tk.PhotoImage(file="Return Car.png")
        self.view_image = tk.PhotoImage(file="View All Cars.png")
        self.save_image = tk.PhotoImage(file="Save to Database.png")
        self.load_image = tk.PhotoImage(file="Load From Database.png")
        self.quit_image = tk.PhotoImage(file="Quit.png")

        # Buttons
        self.button_frame = tk.Frame(root, bg="#2d3142")
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, image=self.add_image, command=self.add_car_window, bg="#2d3142")
        self.add_button.grid(row=0, column=0, padx=5)

        self.remove_button = tk.Button(self.button_frame, image=self.remove_image, command=self.remove_car_window, bg="#2d3142")
        self.remove_button.grid(row=0, column=1, padx=5)

        self.find_button = tk.Button(self.button_frame, image=self.find_image, command=self.find_car_window, bg="#2d3142")
        self.find_button.grid(row=0, column=2, padx=5)

        self.rent_button = tk.Button(self.button_frame, image=self.rent_image, command=self.rent_car_window, bg="#2d3142")
        self.rent_button.grid(row=0, column=3, padx=5)

        self.return_button = tk.Button(self.button_frame, image=self.return_image, command=self.return_car_window, bg="#2d3142")
        self.return_button.grid(row=0, column=4, padx=5)

        self.view_button = tk.Button(self.button_frame, image=self.view_image, command=self.view_all_cars, bg="#2d3142")
        self.view_button.grid(row=1, column=0, padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, image=self.save_image,
                                     command=lambda: self.inventory.save_to_database("inventory.csv"), bg="#2d3142")
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        self.load_button = tk.Button(self.button_frame, image=self.load_image,
                                     command=lambda: self.inventory.load_from_database("inventory.csv"), bg="#2d3142")
        self.load_button.grid(row=1, column=2, padx=5, pady=5)

        self.quit_button = tk.Button(self.button_frame, image=self.quit_image, command=self.root.quit, bg="#2d3142")
        self.quit_button.grid(row=1, column=3, padx=5, pady=5)

        self.load_initial_data()

    def load_initial_data(self):
        self.inventory.load_from_database("inventory.csv")

    def add_car_window(self):
        self.open_input_window("Add Car", self.add_car)

    def remove_car_window(self):
        self.open_input_window("Remove Car", self.remove_car, single_field="plate")

    def find_car_window(self):
        self.open_input_window("Find Car", self.find_car, single_field="plate")

    def rent_car_window(self):
        self.open_input_window("Rent Car", self.rent_car, single_field="plate")

    def return_car_window(self):
        self.open_input_window("Return Car", self.return_car, single_field="plate")

    def open_input_window(self, title, submit_function, single_field=None):
        input_window = tk.Toplevel(self.root)
        input_window.title(title)
        input_window.configure(bg="#f0f0f0")

        if single_field:
            entry_label = tk.Label(input_window, text=f"Enter {single_field.capitalize()}:", bg="#f0f0f0")
            entry_label.pack()
            entry = tk.Entry(input_window)
            entry.pack()
            fields = [entry]
        else:
            fields = []
            for label in ["Plate", "Make", "Model", "Year", "Mileage"]:
                tk.Label(input_window, text=f"Enter {label}:", bg="#f0f0f0").pack()
                entry = tk.Entry(input_window)
                entry.pack()
                fields.append(entry)

        def validate_int(value, field_name):
            try:
                return int(value)
            except ValueError:
                messagebox.showerror("Input Error", f"{field_name} must be an integer.")
                return None

        def on_submit():
            if single_field:
                submit_function(fields[0].get())
            else:
                year = validate_int(fields[3].get(), "Year")
                mileage = validate_int(fields[4].get(), "Mileage")
                if year is None or mileage is None:
                    return
                submit_function(fields[0].get(), fields[1].get(), fields[2].get(), year, mileage)
            input_window.destroy()

        submit_button = tk.Button(input_window, text="Submit", command=on_submit, bg="#4CAF50", fg="white")
        submit_button.pack()

    def add_car(self, plate, make, model, year, mileage):
        car = Car(plate, make, model, year, mileage)
        message = self.inventory.add_car(car)
        messagebox.showinfo("Result", message)

    def remove_car(self, plate):
        message = self.inventory.remove_car(plate)
        messagebox.showinfo("Result", message)

    def find_car(self, plate):
        car = self.inventory.find_car(plate)
        if car:
            rental_status = "Rented" if car.rented else "Available"
            message = f"Plate: {car.plate}\nMake: {car.make}\nModel: {car.model}\n" \
                      f"Year: {car.year}\nMileage: {car.mileage}\nStatus: {rental_status}"
        else:
            message = "Car not found."
        messagebox.showinfo("Find Car", message)

    def rent_car(self, plate):
        message = self.inventory.rent_car(plate)
        messagebox.showinfo("Result", message)

    def return_car(self, plate):
        message = self.inventory.return_car(plate)
        messagebox.showinfo("Result", message)

    def view_all_cars(self):
        cars = self.inventory.cars
        if not cars:
            message = "No cars in the inventory."
        else:
            message = "\n".join(
                f"Plate: {car.plate}, Make: {car.make}, Model: {car.model}, Year: {car.year}, "
                f"Mileage: {car.mileage}, Status: {'Rented' if car.rented else 'Available'}"
                for car in cars
            )
        view_window = tk.Toplevel(self.root)
        view_window.title("All Cars")
        view_window.configure(bg="#0B3DA7")
        text_widget = tk.Text(view_window, wrap=tk.WORD, width=80, height=20, bg="#ffffff", fg="#000000")
        text_widget.insert(tk.END, message)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(padx=10, pady=10)

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    gui = InventoryGUI(root)
    root.mainloop()

