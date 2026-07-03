# 🧾 Invoice Generator

A professional Invoice Management System built using **Python**, **Flask**, **Peewee ORM**, **SQLite**, **Bulma CSS**, **Redis**, and **Celery**.

The application allows users to manage customers, products, and invoices, generate professional PDF invoices, cache dashboard data using Redis, and automatically send invoice due reminders using Celery.

---

# Features

## Customer Management
- Add new customers
- View customer list

## Item Management
- Add items with prices
- Edit items
- Delete items
- View item list

## Invoice Management
- Create invoices for customers
- Select multiple existing items
- Add custom items manually
- Specify quantity for each item
- Automatic subtotal calculation
- Tax percentage support
- Automatic tax calculation
- Grand total calculation
- Due date support
- Invoice status (Pending / Paid / Overdue)

## Invoice Details
- View complete invoice
- Customer information
- Invoice items
- Tax summary
- Total amount
- Mark invoice as Paid

## PDF Generation
- Generate professional invoice PDF
- Customer details
- Invoice summary
- Items table
- Download invoice

## Dashboard
- Total Customers
- Total Items
- Total Invoices
- Recent invoices

## Redis Cache
Dashboard statistics are cached using Redis to reduce unnecessary database queries.

Cached values:
- Customer Count
- Item Count
- Invoice Count

## Celery Reminder System
Celery automatically checks invoices.

If an invoice is due today and is still pending, a reminder is generated.

Example:

```
Reminder!

Invoice ID : 3

Customer : sanket

Total : ₹8,496,000

Due Today!
```

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Flask | Web Framework |
| Peewee ORM | Database ORM |
| SQLite | Database |
| Jinja2 | HTML Templates |
| Bulma CSS | UI Styling |
| ReportLab | PDF Generation |
| Redis | Caching |
| Celery | Background Tasks |

---

## 📂 Project Structure

```text
INVOICE_TASK1-MAIN/
│
├── __pycache__/
│
├── templates/
│   ├── customers/
│   │   ├── form.html
│   │   └── list.html
│   │
│   ├── invoices/
│   │   ├── details.html
│   │   ├── form.html
│   │   └── list.html
│   │
│   ├── items/
│   │
│   ├── base.html
│   └── index.html
│
├── venv/
│
├── app.py
├── celery_app.py
├── celerybeat-schedule
├── database.py
├── invoice_1.pdf
├── invoice_3.pdf
├── invoice.pdf
├── invoice.db
├── models.py
├── redis_client.py
├── requirements.txt
└── tasks.py

```
---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd invoice_generator
```

---

## Create Virtual Environment

### Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Flask Application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

# Redis Setup

Start Redis

Linux

```bash
sudo systemctl start redis
```

Verify

```bash
redis-cli
```

```
PING
```

Output

```
PONG
```

---

# Celery Worker

Start worker

```bash
celery -A celery_app worker --loglevel=info
```

---

# Celery Beat

Start scheduler

```bash
celery -A celery_app beat --loglevel=info
```

---

# Screenshots

## Dashboard

<img width="1433" height="846" alt="Screenshot from 2026-07-03 11-12-27" src="https://github.com/user-attachments/assets/a3c21c93-342f-4deb-8f16-b24c320d8fc9" />


---

## Customers

<img width="1433" height="846" alt="Screenshot from 2026-07-03 11-12-35" src="https://github.com/user-attachments/assets/c752264a-25e4-4526-9040-c77f8ae9a0d7" />


---

## Items

<img width="1433" height="846" alt="Screenshot from 2026-07-03 11-12-41" src="https://github.com/user-attachments/assets/ae22c0b2-8361-4475-8acc-eba1ebd79fed" />

---
## Invoice List

<img width="1433" height="846" alt="Screenshot from 2026-07-03 11-12-59" src="https://github.com/user-attachments/assets/58b33055-002d-496d-8804-eca4cdb57194" />




---
## Create Invoice

<img width="1433" height="846" alt="Screenshot from 2026-07-03 11-13-14" src="https://github.com/user-attachments/assets/e9d98415-a7ef-4076-84b2-9302c09cee03" />

---

## Invoice Details

<img width="1433" height="846" alt="Screenshot from 2026-07-03 11-13-39" src="https://github.com/user-attachments/assets/3161f8e1-1960-44d2-8497-6a3a5372bc3b" />


---

## Invoice PDF

<img width="938" height="1079" alt="Screenshot from 2026-07-03 11-29-39" src="https://github.com/user-attachments/assets/0515b2ca-5dc8-42ea-9deb-87007dee06ab" />

---

## Celery Reminder

<img width="1317" height="467" alt="Screenshot from 2026-07-03 11-11-07" src="https://github.com/user-attachments/assets/96f314c9-1fe6-44cc-832c-9aca8dfd6713" />

---

# Future Improvements

- Email invoices to customers
- Payment Gateway Integration
- GST Invoice Support
- QR Code for Payments
- Company Logo Upload
- User Authentication
- Search & Filters
- Monthly Sales Reports
- Charts and Analytics
- Export to Excel

---

# Author

**Paras Gogia**
---
