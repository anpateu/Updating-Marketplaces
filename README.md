# API Manager for marketplaces

This project is a Python-based Product Information Management system that retrieves data on product prices and stock levels from an Excel file received via email, as well as through APIs from the MoySklad inventory management system, Ozon marketplace, and Wildberries marketplace.

## Functionality
The system's main functionality includes the following:

- Retrieval of product data from an Excel file received via email.
- Retrieval of product data from the MoySklad inventory management system using their API.
- Retrieval of product data from the Ozon marketplace using their API.
- Retrieval of product data from the Wildberries marketplace using their API.
- Storage of product data in a SQLite database.
- Updating of the product data in the database based on new data retrieved from MoySklad, Ozon, and Wildberries.
- Retrieval of additional product data from a separate system called AutoElectrica.

## Usage
Once the system is running, it will automatically retrieve new data from the MoySklad, Ozon, and Wildberries APIs on an hourly basis, and update the database accordingly. The system will also retrieve additional product data from AutoElectrica on a daily basis.
