from flask import Flask,render_template,request,redirect,send_file
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table as PDFTable,
    TableStyle
)

from redis_client import r

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

from flask import send_file

import os

from models import *

app = Flask(__name__)


def update_invoice_status():

    invoices = Invoice.select()

    for invoice in invoices:

        if invoice.status == "Paid":
            continue

        if invoice.due_date < date.today():

            invoice.status = "Overdue"

        else:

            invoice.status = "Pending"

        invoice.save()

# dashboard
@app.route("/")
def dashboard():
    update_invoice_status()

    customer_count = r.get("customer_count")

    if customer_count is None:
        customer_count = Customer.select().count()
        r.set(
            "customer_count",
            customer_count,
            ex=600
        )

    item_count = r.get("item_count")

    if item_count is None:
        item_count = Item.select().count()
        r.set(
            "item_count",
            item_count,
            ex=600
        )

    invoice_count = r.get("invoice_count")

    if invoice_count is None:
        invoice_count = Invoice.select().count()
        r.set(
            "invoice_count",
            invoice_count,
            ex=600
        )

    invoices = Invoice.select().order_by(
        Invoice.id.desc()
    ).limit(5)

    return render_template(
        "index.html",
        customer_count=customer_count,
        item_count=item_count,
        invoice_count=invoice_count,
        invoices=invoices
    )

# customers routes
@app.route("/customers")
def customers():

    data = Customer.select()

    return render_template("customers/list.html",customers = data)


@app.route("/customers/add",
methods=["GET","POST"])
def add_customer():

    if request.method == "POST":

        Customer.create(
            name=request.form["name"],
            email=request.form["email"],
            phone=request.form["phone"]
        )
        r.delete("customer_count")
        return redirect("/customers")
    
    return render_template(
        "customers/form.html"
    )

# items routes
@app.route("/items")
def items():

    items = Item.select()

    return render_template("items/list.html",items=items)


@app.route("/items/add",
methods=["GET","POST"])
def add_item():

    if request.method == "POST":

        Item.create(
            name=request.form["name"],
            price=request.form["price"]
        )
        
        r.delete("item_count")
        return redirect("/items")
    
    
    return render_template("items/form.html")


@app.route("/items/delete/<int:id>")
def delete_item(id):

    item = Item.get_by_id(id)

    item.delete_instance()
    
    r.delete("item_count")

    return redirect("/items")


@app.route("/items/edit/<int:id>",
methods=["GET","POST"])
def edit_item(id):

    item = Item.get_by_id(id)

    if request.method == "POST":

        item.name = request.form["name"]

        item.price = request.form["price"]

        item.save()
        
        r.delete("item_count")
        
        return redirect("/items")
    
    return render_template("items/form.html",item=item)

# invoices routes
@app.route("/invoices")
def invoices():
    
    update_invoice_status()
    invoices = Invoice.select()

    return render_template(
        "invoices/list.html",
        invoices=invoices
    )


@app.route("/invoices/add",
methods=["GET","POST"])
def add_invoice():

    customers = Customer.select()

    items = Item.select()

    if request.method == "POST":

        customer = request.form["customer"]
        
        due_date = request.form["due_date"]

        tax_percent = float(
            request.form["tax"] or 0
        )

        invoice = Invoice.create(
            customer=customer,
            due_date=due_date,
            tax_percent=tax_percent
        )

        subtotal = 0

        selected_items = request.form.getlist("items")

        for item_id in selected_items:


            item = Item.get_by_id(item_id)


            qty = int(
                request.form[
                    f"qty_{item.id}"
                ]
            )

            InvoiceItem.create(

                invoice=invoice,

                item_name=item.name,

                price=item.price,

                quantity=qty
            )

            subtotal += item.price * qty

        custom_name = request.form["custom_name"]

        custom_price = request.form["custom_price"]

        if custom_name and custom_price:

            price = float(custom_price)

            InvoiceItem.create(

                invoice=invoice,

                item_name=custom_name,

                price=price,

                quantity=1

            )

            subtotal += price

        tax_amount = (
            subtotal * tax_percent / 100
        )

        invoice.subtotal = subtotal

        invoice.tax_amount = tax_amount

        invoice.total = subtotal + tax_amount

        invoice.save()
        
        r.delete("invoice_count")

        return redirect("/invoices")
    
    

    return render_template("invoices/form.html",customers=customers,items=items)


@app.route("/invoices/delete/<int:id>")
def delete_invoice(id):

    invoice = Invoice.get_by_id(id)

    InvoiceItem.delete().where(
        InvoiceItem.invoice == invoice
    ).execute()

    invoice.delete_instance()
    
    r.delete("invoice_count")

    return redirect("/invoices")



@app.route("/invoices/<int:id>")
def invoice_details(id):

    invoice = Invoice.get_by_id(id)

    items = InvoiceItem.select().where(
        InvoiceItem.invoice == invoice
    )

    return render_template("invoices/details.html",invoice=invoice,items=items)



@app.route("/invoice/pdf/<int:id>")
def invoice_pdf(id):

    invoice = Invoice.get_by_id(id)

    items = InvoiceItem.select().where(
        InvoiceItem.invoice == invoice
    )

    filename = f"invoice_{invoice.id}.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading = styles["Heading2"]

    normal = styles["Normal"]

    content = []

    # ==================================================
    # COMPANY HEADER
    # ==================================================

    content.append(
        Paragraph(
            "<b><font size='22'>Korecent Solutions</font></b>",
            title_style
        )
    )

    content.append(
        Paragraph(
            "Invoice Management System",
            styles["Heading3"]
        )
    )

    content.append(
        Paragraph(
            "Email : info@korecent.com",
            normal
        )
    )

    content.append(
        Paragraph(
            "Phone : +91 9876543210",
            normal
        )
    )

    content.append(Spacer(1, 20))

    # ==================================================
    # INVOICE TITLE
    # ==================================================

    content.append(
        Paragraph(
            "<b><font size='20'>TAX INVOICE</font></b>",
            title_style
        )
    )

    content.append(Spacer(1, 20))

    # ==================================================
    # INVOICE DETAILS
    # ==================================================

    content.append(
        Paragraph(
            f"""
            <b>Invoice No:</b> INV-{invoice.id:04d}<br/>
            <b>Invoice Date:</b> {invoice.date}<br/>
            <b>Due Date:</b> {invoice.due_date}<br/>
            <b>Status:</b> {invoice.status}
            """,
            normal
        )
    )

    content.append(Spacer(1, 15))

    # ==================================================
    # CUSTOMER DETAILS
    # ==================================================

    content.append(
        Paragraph(
            "<b><font size='14'>Bill To</font></b>",
            heading
        )
    )

    content.append(
        Paragraph(
            f"""
            <b>{invoice.customer.name}</b><br/>
            {invoice.customer.email}<br/>
            {invoice.customer.phone}
            """,
            normal
        )
    )

    content.append(Spacer(1, 20))

    # ==================================================
    # ITEMS TABLE
    # ==================================================

    data = [
        [
            "Item",
            "Unit Price",
            "Qty",
            "Total"
        ]
    ]

    for item in items:

        data.append([
            item.item_name,
            f"Rs. {item.price:,.2f}",
            item.quantity,
            f"Rs. {(item.price * item.quantity):,.2f}"
        ])

    table = PDFTable(
        data,
        colWidths=[180,110,70,120]
    )

    table.setStyle(
        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0F62FE")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("FONTSIZE",(0,0),(-1,0),12),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

            ("TOPPADDING",(0,0),(-1,0),10),

            ("ALIGN",(1,1),(-1,-1),"CENTER"),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE")

        ])
    )

    content.append(table)

    content.append(Spacer(1, 25))

    # ==================================================
    # TOTALS TABLE
    # ==================================================

    totals = [

        ["Subtotal", f"Rs. {invoice.subtotal:,.2f}"],

        ["Tax", f"{invoice.tax_percent}%"],

        ["Tax Amount", f"Rs. {invoice.tax_amount:,.2f}"],

        ["Grand Total", f"Rs. {invoice.total:,.2f}"]

    ]

    total_table = PDFTable(
        totals,
        colWidths=[180,180]
    )

    total_table.setStyle(
        TableStyle([

            ("BACKGROUND",(0,3),(-1,3),colors.HexColor("#D9EDF7")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("ALIGN",(1,0),(-1,-1),"RIGHT"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8)

        ])
    )

    content.append(total_table)

    content.append(Spacer(1, 40))

    # ==================================================
    # FOOTER
    # ==================================================

    content.append(
        Paragraph(
            "<b>Thank you for your business!</b>",
            title_style
        )
    )

    content.append(
        Paragraph(
            "This is a computer generated invoice and does not require a signature.",
            normal
        )
    )

    doc.build(content)

    return send_file(
        os.path.abspath(filename),
        as_attachment=True,
        download_name=filename
    )
    
    
@app.route("/invoice/paid/<int:id>")
def mark_invoice_paid(id):

    invoice = Invoice.get_by_id(id)

    if invoice.status != "Paid":

        invoice.status = "Paid"
        invoice.save()

    return redirect(f"/invoices/{id}")
    
if __name__ == "__main__":
    db.connect()
        
    db.create_tables([Customer,Item,Invoice,InvoiceItem])
        
    app.run(debug=True)

    