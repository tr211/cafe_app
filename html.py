from tkinter import messagebox
from app import customer_dict
import os

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
