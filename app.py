from collections import defaultdict
import customtkinter as ctk
import json
from datetime import datetime
from tkinter import messagebox, simpledialog
import logging
import webbrowser
import csv
import os

# Initialize Logging
logging.basicConfig(filename='coffee_shop.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Global Variables
CUSTOMERS_JSON = "customers.json"
REPORT_DIR = "report"
CLIENTS_DIR = "clients"
customer_dict = defaultdict(lambda: {'quantity_coffee': 0, 'mobile_number': '', 'purchase_history': []})

# Set Theme
ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("green")  # Options: "blue", "green", "dark-blue"

# Load Data
def load_data():
    try:
        with open(CUSTOMERS_JSON, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data():
    with open(CUSTOMERS_JSON, "w") as file:
        json.dump(customer_dict, file, indent=4)

def count_coffee(quantity_coffee):
    total = sum(quantity_coffee)
    free_coffees = total // 8  # Every 8th coffee is free
    return total + free_coffees

customer_dict = load_data()

# Function to log purchase history
def log_purchase(name, quantity):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    customer_dict[name]['purchase_history'].append({'quantity': quantity, 'timestamp': timestamp})
    save_data()
    if customer_dict[name]['quantity_coffee'] >= 8:
        messagebox.showinfo("Reward Alert", f"{name} reached 8 coffees! Enjoy a free one!")

# Analytics Dashboard
def show_analytics():
    total_coffees = sum(details['quantity_coffee'] for details in customer_dict.values())
    top_customer = max(customer_dict.items(), key=lambda x: x[1]['quantity_coffee'], default=("None", {}))[0]
    month = datetime.now().strftime("%Y-%m")
    messagebox.showinfo("Analytics Dashboard", f"Total Coffees Sold: {total_coffees}\nTop Customer: {top_customer}\nMonth: {month}")

# Refresh customer list in UI
def refresh_customer_list():
    customer_listbox.delete("1.0", ctk.END)
    for name, details in customer_dict.items():
        customer_listbox.insert(ctk.END, f"{name} - Mobile: {details['mobile_number']} - Coffee: {details['quantity_coffee']}\n")

# Add customer with history tracking
def add_customer():
    name = name_entry.get().strip()
    mobile = mobile_entry.get().strip()
    coffee_text = coffee_entry.get().strip()

    if not name or not mobile or not coffee_text:
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return
    try:
        mobile_number = int(mobile)
        if len(str(mobile_number)) != 10:
            raise ValueError("Mobile number must be 10 digits.")
        coffee_quantity = list(map(int, coffee_text.split(',')))
    except ValueError as e:
        messagebox.showwarning("Input Error", f"Invalid input! {str(e)}")
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
    name_request = name_entry.get().strip().lower()
    mobile_request = mobile_entry.get().strip()
    
    if not name_request and not mobile_request:
        messagebox.showwarning("Input Error", "Enter a Name or Mobile Number to search!")
        return

    for name, details in customer_dict.items():
        if (name.lower() == name_request) or (str(details['mobile_number']) == mobile_request):
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

# Export customers to CSV
def export_customers_to_csv(filename):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if missing
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Mobile Number', 'Quantity'])
            for name, details in customer_dict.items():
                writer.writerow([name, details['mobile_number'], details['quantity_coffee']])
        messagebox.showinfo("Export Complete", f"Customers exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

# Export customers to JSON
def export_customers_to_json(filename):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if missing
        with open(filename, 'w') as json_file:
            json.dump(customer_dict, json_file, indent=4)
        messagebox.showinfo("Export Complete", f"Customers exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

# Export customers to HTML
def export_customers_to_html(filename):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create directory if missing
        with open(filename, 'w') as html_file:
            # HTML Template
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Monthly Sales Report</title>
                <style>
                    body { font-family: Arial, sans-serif; }
                    h1 { color: #4CAF50; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                    th { background-color: #f2f2f2; }
                    tr:hover { background-color: #f5f5f5; }
                </style>
            </head>
            <body>
                <h1>Monthly Sales Report</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Mobile Number</th>
                            <th>Coffee Quantity</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            # Add rows for each customer
            for name, details in customer_dict.items():
                html_content += f"""
                        <tr>
                            <td>{name}</td>
                            <td>{details['mobile_number']}</td>
                            <td>{details['quantity_coffee']}</td>
                        </tr>
                """
            # Close HTML tags
            html_content += """
                    </tbody>
                </table>
            </body>
            </html>
            """
            html_file.write(html_content)
        messagebox.showinfo("Export Complete", f"Customers exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

# Export customers to JSON and CSV
def export_customers_data():
    try:
        os.makedirs(CLIENTS_DIR, exist_ok=True)
        # Save to JSON
        export_customers_to_json(f'{CLIENTS_DIR}/customers.json')
        # Save to CSV
        export_customers_to_csv(f'{CLIENTS_DIR}/customers.csv')
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

# View Monthly Sales Report (HTML, JSON, and CSV)
def view_monthly_sales_report():
    os.makedirs(REPORT_DIR, exist_ok=True)  # Ensure directory exists
    # Export to CSV
    export_customers_to_csv(f'{REPORT_DIR}/monthly_sales_report.csv')
    # Export to JSON
    export_customers_to_json(f'{REPORT_DIR}/monthly_sales_report.json')
    # Export to HTML
    export_customers_to_html(f'{REPORT_DIR}/monthly_sales_report.html')
    # Open HTML report in browser
    html_file_path = os.path.abspath(f'{REPORT_DIR}/monthly_sales_report.html')  # Get absolute path
    webbrowser.open(f'file://{html_file_path}')  # Use file:// protocol for local files


# Setup UI
def setup_ui(root):
    root.title("Coffee Shop ☕")
    root.geometry("600x500")
    
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Input Fields
    ctk.CTkLabel(frame, text="Customer Name:", font=("Arial", 14)).pack(pady=5)
    global name_entry, mobile_entry, coffee_entry, customer_listbox
    name_entry = ctk.CTkEntry(frame, placeholder_text="Enter name...")
    name_entry.pack(pady=5)

    ctk.CTkLabel(frame, text="Mobile Number:", font=("Arial", 14)).pack(pady=5)
    mobile_entry = ctk.CTkEntry(frame, placeholder_text="Enter number...")
    mobile_entry.pack(pady=5)
    
    ctk.CTkLabel(frame, text="Coffee Quantity:", font=("Arial", 14)).pack(pady=5)
    coffee_entry = ctk.CTkEntry(frame, placeholder_text="e.g. 2,3,1")
    coffee_entry.pack(pady=5)

    # Button Frame to Group Buttons
    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(pady=10)

    # Buttons                                                                  side="left"
    ctk.CTkButton(button_frame, text="Add Customer", command=add_customer).pack(side="top", padx=5, pady=5)
    ctk.CTkButton(button_frame, text="Search Customer", command=search_customer).pack(side="top", padx=5, pady=5)
    ctk.CTkButton(button_frame, text="Export Data", command=export_customers_data).pack(side="top", padx=5, pady=5)
    ctk.CTkButton(button_frame, text="View Monthly Report", command=view_monthly_sales_report).pack(side="top", padx=5, pady=5)

    # Customer Listbox
    customer_listbox = ctk.CTkTextbox(frame, height=200, width=500)
    customer_listbox.pack(pady=10)
    refresh_customer_list()

    # Bind Enter key
    root.bind('<Return>', lambda event: add_customer() if name_entry.get() and mobile_entry.get() else search_customer())

if __name__ == "__main__":
    root = ctk.CTk()
    setup_ui(root)
    root.mainloop()