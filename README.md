# Django Bonus Management System

----------------------------------
Project Overview
---------------------------------
This project is a Django-based web application for managing supplier bonus agreements and promotional discounts.
The system allows management of master data, storing and controlling contract agreements and reporting based on transactional data. 
Managing supplier bonus percentages
Input of purchasing transactions regarding amounts
Importing purchasing data from Excel files
Calculating supplier bonuses
Managing promotional discount conditions
Input of sold quantities for promotional products
Generating promotional report
Each purchasing record is linked to exactly one supplier, while a supplier can have multiple purchasing records.(One-to-Many relationship). Same logic applied to promotional products and their sales quantities
REST API for bonus reporting 
Asynchronous report generation and email sending
Authentication and role-based access control
Deployment on Azure cloud environment

The application is built using Django.
PostgreSQL is used for local development, while SQLite is used in the deployed Azure environment.

-------------------------------
Python 3.12
PostgreSQL 14 or higher (tested with PostgreSQL 17)

-------------------------------
Deployment (Azure)
-------------------------------
The application is deployed and accessible via Microsoft Azure App Service.
The deployed version is used for evaluation and reflects the latest version of the project from the GitHub repository.
Production configuration includes:
- Gunicorn as application server
- Environment variables for sensitive data
- Static file handling with WhiteNoise
- DEBUG set to False
- SQLite database (Azure temporary storage)
- Email service configured via SMTP provider
- Email sending via SMTP (SendGrid or similar provider)

-------------------------------
Application URL
-------------------------------
Live Demo:
https://www.bonusapp-bg.eu

-------------------------------
Database Config
-------------------------------
The project uses different databases depending on the environment:

Local Development:
PostgreSQL is used with environment variables.

Production (Azure):
SQLite is used as a lightweight database stored in the Azure environment.

Environment variables are required for local testing.

Note: The .env file is not included in the repository for security reasons.

Create a .env file in the root directory with the following variables:

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASS=your_database_password
DB_PORT=5432
DB_HOST=127.0.0.1

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
Authentication & User Management
----------------------------------------
Implemented custom user model (AppUser)
User registration, login and logout functionality
Role-based access control (e.g. manager permissions)
Public vs private access (some pages require authentication)

-----------------------------------------
REST API for Bonus Reporting
----------------------------------------
Added API endpoint for bonus report using Django REST Framework
JSON response for external integrations
Secured access with authentication permissions
-----------------------------------------

Asynchronous Report Generation & Email Sending
----------------------------------------
Implemented automated report generation using background task processing.
Designed to support asynchronous execution (e.g. Celery), but currently executed synchronously in the deployed environment.

-----------------------------------------
Testing
----------------------------------------
Added unit tests for:
Business logic
Views
User functionality

-----------------------------------------
Environment Variables (Azure)
----------------------------------------
Environment variables are configured in Azure App Service under:

Settings → Environment Variables

Configured variables include:
- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- CSRF_TRUSTED_ORIGINS
- Database credentials (DB_NAME, DB_USER, DB_PASS, DB_PORT)
- AZURE_POSTGRESQL_CONNECTIONSTRING

These variables are used to securely configure the application in production.

-----------------------------------------
Production Limitations
----------------------------------------
SQLite database is stored in temporary storage and may be reset
Celery/Redis is not configured in the deployed environment
Email functionality requires a verified SMTP sender

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
