from flask import Flask,render_template,request,redirect,send_file

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

# dashboard
@app.route("/")
def dashboard():

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
        return redirect("/items")
    
    return render_template("items/form.html")


@app.route("/items/delete/<int:id>")
def delete_item(id):

    item = Item.get_by_id(id)

    item.delete_instance()

    return redirect("/items")


@app.route("/items/edit/<int:id>",
methods=["GET","POST"])
def edit_item(id):

    item = Item.get_by_id(id)

    if request.method == "POST":

        item.name = request.form["name"]

        item.price = request.form["price"]

        item.save()

        return redirect("/items")

    return render_template("items/form.html",item=item)

# invoices routes
@app.route("/invoices")
def invoices():

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

        tax_percent = float(
            request.form["tax"] or 0
        )

        invoice = Invoice.create(
            customer=customer,

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

        return redirect("/invoices")

    return render_template("invoices/form.html",customers=customers,items=items)


@app.route("/invoices/delete/<int:id>")
def delete_invoice(id):

    invoice = Invoice.get_by_id(id)

    InvoiceItem.delete().where(
        InvoiceItem.invoice == invoice
    ).execute()

    invoice.delete_instance()

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


    filename = "invoice.pdf"


    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )


    styles = getSampleStyleSheet()


    data = [
        [
            "Item",
            "Price",
            "Qty",
            "Total"
        ]
    ]


    for item in items:

        data.append(
            [
                item.item_name,
                item.price,
                item.quantity,
                item.price * item.quantity
            ]
        )

    table = PDFTable(data)

    table.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),1,None)
        ])
    )

    content = []

    content.append(
        Paragraph(
            "INVOICE",
            styles["Title"]
        )
    )

    content.append(Spacer(1,20))

    content.append(
        Paragraph(
            f"""
            Invoice ID: {invoice.id}<br/>
            Customer: {invoice.customer.name}<br/>
            Date: {invoice.date}
            """,
            styles["Normal"]
        )
    )

    content.append(Spacer(1,20))

    content.append(table)

    content.append(Spacer(1,20))

    content.append(
        Paragraph(
            f"""
            Subtotal: {invoice.subtotal}<br/>
            Tax: {invoice.tax_percent}%<br/>
            Tax Amount: {invoice.tax_amount}<br/>
            Total: {invoice.total}
            """,
            styles["Normal"]
        )
    )

    doc.build(content)

    return send_file(
        os.path.abspath(filename),
        as_attachment=True
    )
    
if __name__ == "__main__":
    db.connect()
        
    db.create_tables([Customer,Item,Invoice,InvoiceItem])
        
    app.run(debug=True)

    