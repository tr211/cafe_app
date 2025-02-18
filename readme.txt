# Coffee Shop Manager

This application is a Coffee Shop Manager built with Python and `customtkinter`. It provides an interface for managing customers, tracking coffee sales, and generating reports.

## Features
- Add new customers with mobile number and coffee quantities.
- Search for existing customers.
- Automatically calculate free coffee rewards (1 free for every 8 purchased).
- Export customer data to CSV and JSON.
- View monthly sales reports and customer tables via a web browser.

## Installation
1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd coffee-shop-manager
    ```
2. Install the dependencies:
    ```bash
    pip install customtkinter
    ```

## Usage
Run the application with:
```bash
python app.py
```

## Folder Structure
- `customers.json`: Stores customer information.
- `clients/`: Contains exported JSON and CSV files of customer data.
- `report/`: Contains reports like monthly sales and customer tables.

## Application Logic
- The application tracks customer purchases and calculates free coffees automatically.
- Data is logged in `coffee_shop.log`.
- Reports are opened automatically in the default web browser.

## Improvements
- Unified `export_customers_to_csv` for cleaner code.
- Implemented a dynamic report viewing feature.


## License
This project is licensed under the MIT License.

