from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "invoice_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.imports = (
    "tasks",
)

celery.conf.timezone = "Asia/Kolkata"

celery.conf.beat_schedule = {

    "invoice-reminder": {

        "task": "tasks.check_due_invoices",

        "schedule": 60.0
    }

}