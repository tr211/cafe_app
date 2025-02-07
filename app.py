import customtkinter as ctk
import json
from datetime import datetime
from tkinter import messagebox, simpledialog

# Set Theme
ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("green")  # Options: "blue", "green", "dark-blue"

# Load Data
def load_data():
    try:
        with open("customers.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):  # Handle file errors
        return {}

def save_data():
    with open("customers.json", "w") as file:
        json.dump(customer_dict, file, indent=4)  # Pretty print JSON

def count_coffee(quantity_coffee):
    total = sum(quantity_coffee)
    free_coffees = total // 8  # Every 8th coffee is free
    return total + free_coffees

customer_dict = load_data()

# Handle Enter Key Press
def on_enter(event):
    if root.focus_get() == name_entry:
        search_customer()
    elif root.focus_get() in (mobile_entry, coffee_entry):
        add_customer()

# UI Functions
def add_customer():
    name = name_entry.get().strip()
    mobile = mobile_entry.get().strip()
    coffee_text = coffee_entry.get().strip()

    if not name or not mobile or not coffee_text:
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return
    try:
        mobile_number = int(mobile)
        coffee_quantity = list(map(int, coffee_text.split(',')))
    except ValueError:
        messagebox.showwarning("Input Error", "Invalid input! Enter numbers correctly.")
        return
    
    customer_dict[name] = {
        "mobile_number": mobile_number,
        "quantity_coffee": count_coffee(coffee_quantity),
        "last_updated": datetime.now().strftime("%Y-%m")
    }
    save_data()
    messagebox.showinfo("Success", f"Customer {name} added successfully!")
    refresh_customer_list()

def search_customer():
    query = name_entry.get().strip().lower()
    if not query:
        messagebox.showwarning("Input Error", "Enter a Name or Mobile Number to search!")
        return

    for name, details in customer_dict.items():
        if name.lower() == query or str(details['mobile_number']) == query:
            update_coffee_quantity(name, details)
            return
    
    messagebox.showwarning("Not Found", "Customer not found!")

def update_coffee_quantity(name, details):
    additional_coffee = simpledialog.askinteger(
        "Update Coffee",
        f"Customer: {name}\nMobile: {details['mobile_number']}\nCurrent Coffee: {details['quantity_coffee']}\n\nEnter additional coffee amount:")

    if additional_coffee is not None:
        customer_dict[name]["quantity_coffee"] += additional_coffee
        save_data()
        messagebox.showinfo("Updated", "Coffee quantity updated successfully!")
        refresh_customer_list()

def refresh_customer_list():
    customer_listbox.delete("1.0", ctk.END)  # Correct way to delete text in CTkTextbox
    for name, details in customer_dict.items():
        customer_listbox.insert(
            ctk.END, f"{name} - Mobile: {details['mobile_number']} - Coffee: {details['quantity_coffee']}\n")

def setup_ui(root):
    root.title("Coffee Shop ☕")
    root.geometry("600x500")
    
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    ctk.CTkLabel(frame, text="Customer Name:", font=("Arial", 14)).pack(pady=5)
    global name_entry, mobile_entry, coffee_entry, customer_listbox
    name_entry = ctk.CTkEntry(frame, placeholder_text="Enter name...")
    name_entry.pack(pady=5)
    
    ctk.CTkLabel(frame, text="Mobile Number:", font=("Arial", 14)).pack(pady=5)
    mobile_entry = ctk.CTkEntry(frame, placeholder_text="Enter number...")
    mobile_entry.pack(pady=5)
    
    ctk.CTkLabel(frame, text="Coffee Quantity (comma-separated):", font=("Arial", 14)).pack(pady=5)
    coffee_entry = ctk.CTkEntry(frame, placeholder_text="e.g. 2,3,1")
    coffee_entry.pack(pady=5)
    
    ctk.CTkButton(frame, text="Add Customer", command=add_customer).pack(pady=10)
    ctk.CTkButton(frame, text="Search Customer", command=search_customer).pack(pady=5)
    
    customer_listbox = ctk.CTkTextbox(frame, height=200, width=500)
    customer_listbox.pack(pady=10)
    refresh_customer_list()

    # Bind Enter key
    root.bind("<Return>", on_enter)

if __name__ == "__main__":
    root = ctk.CTk()
    setup_ui(root)
    root.mainloop()
