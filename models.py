from peewee import *

from database import db
from datetime import date

class BaseModel(Model):

    class Meta:
        database = db


class Customer(BaseModel):

    name = CharField()
    email = CharField()
    phone = CharField()


class Item(BaseModel):

    name = CharField()
    price = FloatField()


class Invoice(BaseModel):

    customer = ForeignKeyField(Customer)
    date = DateField(default=date.today)

    subtotal = FloatField(default=0)

    tax_percent = FloatField(default=0)

    tax_amount = FloatField(default=0)

    total = FloatField(default=0)


class InvoiceItem(BaseModel):

    invoice = ForeignKeyField(Invoice)

    item_name = CharField()

    price = FloatField()

    quantity = IntegerField()    

    