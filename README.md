# Invoice Generator

A full-stack Invoice Generator built with Flask, Peewee ORM, SQLite, Redis, and Bulma CSS.

## Features

- Customer Management
- Item Management
- Invoice Creation
- Multiple Item Selection
- Tax Calculation
- Invoice Details Page
- PDF Invoice Generation
- Dashboard
- Redis Caching

## Tech Stack

- Python
- Flask
- Peewee ORM
- SQLite
- Redis
- ReportLab
- Bulma CSS

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd invoice_generator
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Redis

```bash
redis-server
```

### Run Flask

```bash
python app.py
```

Visit:

```
http://127.0.0.1:5000
```

## Folder Structure

```
invoice_generator/
│
├── app.py
├── models.py
├── database.py
├── redis_client.py
├── tasks.py
├── templates/
├── static/
├── invoice.db
└── README.md
```

## Future Improvements

- Email Notifications
- Celery Beat Scheduler
- Payment Tracking
- Invoice Status (Paid/Pending)
- Search and Filters
- Authentication
- Company Profile
- GST Support
- REST API
