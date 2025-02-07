Customer Management:

Add new customers with their name, mobile number, and coffee quantities.

Search for customers by name or mobile number.

Update the coffee quantity for existing customers.

Display all customers in a listbox.

Coffee Calculation:

Every 8th coffee is free, and the total coffee count is calculated accordingly.

Monthly Update:

Automatically resets the coffee quantity for all customers at the start of a new month.

Data Persistence:

Customer data is saved to a JSON file (customers.json) and loaded when the program starts.

User-Friendly GUI:

Input fields for name, mobile number, and coffee quantities.

Buttons for adding, searching, and displaying customers.

A listbox to display all customers.

Code Structure
Core Functions:

count_coffee: Calculates the total coffee count, including free coffees.

add_customer: Adds a new customer to the dictionary.

search_customer: Searches for a customer by name or mobile number.

update_coffee_quantity: Updates the coffee quantity for a customer.

get_all_customers: Returns all customers.

update_monthly: Resets coffee quantities at the start of a new month.

save_data and load_data: Handles saving and loading customer data to/from a JSON file.

GUI Functions:

setup_ui: Sets up the main window and UI components.

load_coffee_icon: Loads and displays a coffee icon.

create_input_frame: Creates input fields for name, mobile number, and coffee quantities.

create_buttons: Creates buttons for adding, searching, and displaying customers.

create_customer_listbox: Creates a listbox to display customer data.

add_customer_gui: Handles adding a new customer via the GUI.

search_customer_gui: Handles searching for a customer via the GUI.

update_coffee_quantity_gui: Updates the coffee quantity for a customer via a dialog box.

show_customers_gui: Displays all customers in the listbox.

get_input_values: Retrieves input values from the entry fields.

validate_inputs: Validates user inputs.

clear_entries: Clears all input fields.

Main Application:

Loads customer data and updates monthly coffee quantities.

Initializes the tkinter main window and starts the GUI.

How It Works
Adding a Customer:

Enter the customer's name, mobile number, and coffee quantities (comma-separated) in the input fields.

Click the "Add Customer" button to save the customer.

Searching for a Customer:

Enter the customer's name or mobile number in the name field.

Click the "Search Customer" button to find the customer.

If found, a dialog box will appear to update the coffee quantity.

Displaying All Customers:

Click the "Show All Customers" button to display all customers in the listbox.

Monthly Reset:

At the start of a new month, the coffee quantities for all customers are reset to 0.