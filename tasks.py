from datetime import date

from celery_app import celery

from models import Invoice


@celery.task
def check_due_invoices():

    print("Checking invoices...")

    invoices = Invoice.select()

    for invoice in invoices:

        if invoice.status == "Paid":
            continue

        if invoice.due_date == date.today():

            print(f"""
Reminder!

Invoice ID : {invoice.id}

Customer : {invoice.customer.name}

Total : ₹{invoice.total}

Due Today!
""")