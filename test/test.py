import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
from typing import List, Dict, Any
from datetime import datetime
from PIL import Image, ImageTk


class Guest:
    def __init__(self, name: str, mobile_number: int, quantity_coffee: List[int]) -> None:
        self.name = name
        self.mobile_number = mobile_number
        self.quantity_coffee = self.count_coffee(quantity_coffee)
        self.last_updated = datetime.now().strftime("%Y-%m")

    def count_coffee(self, quantity_coffee: List[int]) -> int:
        total = sum(quantity_coffee)
        free_coffees = total // 8  # Every 8th coffee is free
        return total + free_coffees


class Customers:
    def __init__(self):
        self.customer_dict: Dict[str, Dict[str, Any]] = {}
        self.load_data()

    def add_customer(self, guest: Guest):
        self.customer_dict[guest.name] = {
            "mobile_number": guest.mobile_number,
            "quantity_coffee": guest.quantity_coffee,
            "last_updated": guest.last_updated
        }
        self.save_data()

    def search_customer(self, query: str) -> Dict[str, Any]:
        for name, details in self.customer_dict.items():
            if name.lower() == query.lower() or str(details['mobile_number']) == query:
                return {"name": name, **details}
        return {}

    def update_coffee_quantity(self, name: str, additional_coffee: int):
        if name in self.customer_dict:
            self.customer_dict[name]["quantity_coffee"] += additional_coffee
            self.save_data()

    def get_all_customers(self):
        return self.customer_dict

    def update_monthly(self):
        current_month = datetime.now().strftime("%Y-%m")
        for name, details in self.customer_dict.items():
            if details.get("last_updated") != current_month:
                self.customer_dict[name]["quantity_coffee"] = 0
                self.customer_dict[name]["last_updated"] = current_month
        self.save_data()

    def save_data(self):
        try:
            with open("customers.json", "w") as file:
                json.dump(self.customer_dict, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def load_data(self):
        try:
            with open("customers.json", "r") as file:
                self.customer_dict = json.load(file)
        except FileNotFoundError:
            self.customer_dict = {}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")


# GUI Class
class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Shop Customer Management")
        self.root.geometry("600x550")
        self.root.configure(bg="#D2B48C")  # Coffee color theme

        self.customers = Customers()
        self.customers.update_monthly()

        # Load Coffee Icon
        try:
            self.coffee_icon = Image.open("coffee_icon.png")
            self.coffee_icon = self.coffee_icon.resize((50, 50), Image.ANTIALIAS)
            self.coffee_icon = ImageTk.PhotoImage(self.coffee_icon)
            self.icon_label = tk.Label(root, image=self.coffee_icon, bg="#D2B48C")
            self.icon_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load icon: {e}")

        # Frames for better UI
        self.frame = tk.Frame(root, padx=20, pady=20, bg="#FFFFFF", relief=tk.RIDGE, borderwidth=2)
        self.frame.pack(pady=10)

        # Labels
        tk.Label(self.frame, text="Name:", bg="#FFFFFF", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.frame, text="Mobile Number:", bg="#FFFFFF", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.frame, text="Coffee Quantity (comma-separated):", bg="#FFFFFF", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)

        # Entry Fields
        self.name_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.mobile_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.mobile_entry.grid(row=1, column=1, padx=10, pady=5)

        self.coffee_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.coffee_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        btn_style = {"font": ("Arial", 12), "bg": "#8B4513", "fg": "white", "padx": 10, "pady": 5}
        tk.Button(self.frame, text="Add Customer", command=self.add_customer, **btn_style).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.frame, text="Search Customer", command=self.search_customer, **btn_style).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self.frame, text="Show All Customers", command=self.show_customers, **btn_style).grid(row=5, column=0, columnspan=2, pady=5)

        # Customer List Display
        self.customer_listbox = tk.Listbox(self.frame, width=50, height=10, font=("Arial", 12))
        self.customer_listbox.grid(row=6, column=0, columnspan=2, pady=10)

    def add_customer(self):
        name = self.name_entry.get()
        mobile = self.mobile_entry.get()
        coffee = self.coffee_entry.get()

        if not name or not mobile or not coffee:
            messagebox.showwarning("Input Error", "All fields must be filled!")
            return

        try:
            mobile_number = int(mobile)
            coffee_quantity = list(map(int, coffee.split(",")))
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid input! Enter numbers correctly.")
            return

        guest = Guest(name, mobile_number, coffee_quantity)
        self.customers.add_customer(guest)
        messagebox.showinfo("Success", f"Customer {name} added successfully!")
        self.clear_entries()

    def search_customer(self):
        query = self.name_entry.get()

        if not query:
            messagebox.showwarning("Input Error", "Enter a Name or Mobile Number to search!")
            return

        customer = self.customers.search_customer(query)

        if customer:
            additional_coffee = simpledialog.askinteger("Update Coffee", f"Customer Found: {customer['name']}\nMobile: {customer['mobile_number']}\nCurrent Coffee: {customer['quantity_coffee']}\n\nEnter additional coffee amount:")
            if additional_coffee:
                self.customers.update_coffee_quantity(customer['name'], additional_coffee)
                messagebox.showinfo("Updated", "Coffee quantity updated successfully!")
        else:
            messagebox.showwarning("Not Found", "Customer not found!")

    def show_customers(self):
        self.customer_listbox.delete(0, tk.END)
        customers = self.customers.get_all_customers()
        if not customers:
            self.customer_listbox.insert(tk.END, "No customers found.")
            return
        for name, details in customers.items():
            self.customer_listbox.insert(tk.END, f"Name: {name}, Mobile: {details['mobile_number']}, Coffee: {details['quantity_coffee']}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.mobile_entry.delete(0, tk.END)
        self.coffee_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()