# Django Bonus Management System

----------------------------------
Project Overview
---------------------------------
This project is a Django-based web application for managing supplier bonus agreements and promotional discounts.
The system allows management of master data, sotring and controlling contract agreements and reporting based on transactional data. 
Managing supplier bonus percentages
Input of purchasing transactions regarding amounts
Importing purchasing data from Excel files
Calculating supplier bonuses
Managing promotional discount conditions
Input of sold quantities for promotional products
Generating promotional report
Each purchasing record is linked to exactly one supplier, while a supplier can have multiple purchasing records.(One-to-Many relationship). Same logic applied to promotional products and their sales quantities

The application is built using Django and PostgreSQL and follows standard Django project structure and best practices.

-------------------------------
Python 3.12
PostgreSQL 14 or higher (tested with PostgreSQL 17)

-------------------------------
Database Config
-------------------------------
The project uses PostgreSQL as the database engine.

Environment variables are required for local testing.

Note: The .env file is not included in the repository for security reasons.

Create a .env file in the root directory with the following variables:

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASS=your_database_password
DB_PORT=5432

The database host is set to:
127.0.0.1

Make sure PostgreSQL is installed and running locally before starting the project.

--------------------------------
Setup
---------------------------------
Installation & Setup

Create virtual environment
python -m venv .venv

Activate the environment (Windows)
.venv\Scripts\activate

Install dependencies
pip install -r requirements.txt

Apply migrations
python manage.py migrate

Run the development server
python manage.py runserver

Open in browser:
http://127.0.0.1:8000/

-----------------------------------
Project Structure
------------------------------------
The project consists of three Django applications:
bonuspercent - handles supplier bonus agreements, purchasing transactions and categories.
bonuspromo - handles promotional discount conditions and sold quantity tracking.
Import_purchasing_amount - Excel file import for purchasing data.
Shared base template and layout are stored in the shared/ directory.

-----------------------------------
Data Model Structure
----------------------------------
Supplier (Master Data)
Unique supplier EIK
Supplier name
Agreed bonus percentage by contract
Linked categories with suppliers (e.g. Dairy, Meat, Bakery, etc.)
Suppliers and product categories are connected through a Many-to-Many relationship.
This means:
One supplier can be linked to multiple product categories.
One product category can include multiple suppliers.
Django automatically creates an intermediate table to manage this relationship.
This structure allows information regarding supliers' categories in their product portfolio.
Purchasing (Transaction Data) - Reference to Supplier (ForeignKey)
Purchasing amount (value excl. VAT)
Calculated bonus amount
Relationship:
One supplier can have multiple purchasing records.
Each purchasing record is linked to exactly one supplier - (One-to-Many relationship)

Promotional Conditions
Product ID
Product name
Purchasing price
Discount percentage by agreement
Sales Quantity
Reference to promotional product
Sold quantity
Promotional bonus calculation formula:
Total Sold Quantity × Purchasing Price × % Discount

---------------------------------------
Features
--------------------------------------
Add / Edit / Delete Suppliers / Read data in created lists 
Assign Multiple Categories to Suppliers (Many-to-Many)
Add / Edit / Delete Purchasing Records / Read data in created lists 
Supplier Bonus Report
Add / Edit / Delete Promotional Conditions/ Read data in created lists 
Add / Edit / Delete Sold Quantities/ Read data in created lists 
Promotional Bonus Report
Category-based Supplier Report
Excel Import for Purchasing Data
Success notifications using Django Messages Framework
Shared base template layout

-----------------------------------------
Security
----------------------------------------
Database credentials are stored in environment variables
.env file is excluded from version control

--------------------------------------
Author
--------------------------------------
Petya Raychinova
Django Bonus Project – 02.2026
