Python 3.12
PostgreSQL 14 or higher (tested with PostgreSQL 17)

# Django Bonus Project

## Setup

1. Create virtual environment
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py runserver

Note: The .env file is not included in the repository for security reasons.

Data Model Structure

Supplier (Master Data)
Unique supplier EIK (unique identification number)
Supplier name
Agreed bonus percentage

Purchasing (Transaction Data)
Reference to Supplier (ForeignKey)
Purchasing amount (value excl. VAT)
Calculated bonus amount

Each purchasing record is linked to exactly one supplier, while a supplier can have multiple purchasing records.(One-to-Many relationship)

