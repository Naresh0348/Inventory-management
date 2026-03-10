# 📦 Inventory Management System

A robust Django-based Inventory Management System designed to track products, manage suppliers, and handle sales and purchase orders with real-time stock updates.



## 🚀 Features
* **Automated Stock Logic:** Automatic decrementing of stock on sales and incrementing on received purchase orders.
* **Race Condition Protection:** Uses Django `F()` expressions to ensure database integrity during high-traffic sales.
* **Low Stock Alerts:** Built-in threshold logic to identify items running low.
* **PostgreSQL Integration:** Configured for production-grade relational database management.
* **Secure Architecture:** Sensitive credentials (DB passwords, Secret Keys) are managed via environment variables.

---

## 🛠 Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/Naresh0348/Inventory-management.git](https://github.com/Naresh0348/Inventory-management.git)
cd Inventory-management

2. Set up Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

3. Install Dependencies
```bash
pip install -r requirements.txt

4. Environment Configuration
Create a file named .env in the root directory and add your local settings:
DB_NAME=your_postgres_db_name
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_django_secret_key

5. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate

6. Create a Superuser (Admin Access)
```bash
python manage.py createsuperuser

7. Run the Server
```bash
python manage.py runserver

Visit http://127.0.0.1:8000/admin to start managing your inventory!

🏗Database Schema
The system architecture is based on the following models:
Product: Core inventory items with unique SKUs and stock tracking.
Category: Classification for easier inventory sorting.
Supplier: Contact data for vendors providing stock.
Sales: Tracks outgoing stock with validation to prevent overselling.
PurchaseOrder: Manages incoming stock with a status-based workflow (Pending -> Received).

> [!WARNING]
> ### 🛡️ Security First
> This project is configured to keep sensitive data private. 
> - **Database Credentials:** All PostgreSQL passwords and user data are stored in a `.env` file.
> - **Secret Key:** The Django `SECRET_KEY` is pulled from the environment.
> - **Version Control:** The `.env` file is explicitly ignored in `.gitignore`. **Do not remove this restriction.**

👨‍💻 Author
Naresh - Naresh0348
