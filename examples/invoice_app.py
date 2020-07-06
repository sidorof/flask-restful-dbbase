# examples/invoice_app.py
"""
This app provides an example posting child relations with a
parent class through the example of an invoice.

"""
# initialize
from flask import Flask
from flask_restful import Api
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import (
    CollectionModelResource,
    ModelResource,
    MetaResource,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db = DBBase(app)


# define invoice
class Invoice(db.Model):
    __tablename__ = "invoice"

    id = db.Column(db.Integer, nullable=True, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)

    # this is the critical part, it requires either backref or
    #   back_populates
    invoice_items = db.relationship("InvoiceItem", backref="invoice")


class InvoiceItem(db.Model):
    __tablename__ = "invoice_item"

    id = db.Column(db.Integer, nullable=True, primary_key=True)
    invoice_id = db.Column(
        db.Integer, db.ForeignKey("invoice.id"), nullable=False
    )
    part_code = db.Column(db.String, nullable=False)
    units = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float(precision=2), nullable=False)


db.create_all()


# create Invoice resources
class InvoiceResource(ModelResource):
    model_class = Invoice

    # necessary only if the database does not understand
    #   dates in string form -- such as Sqlite3
    use_date_conversions = True


# the rest of the resources
class InvoiceCollectionResource(CollectionModelResource):
    model_class = Invoice


class InvoiceItemResource(ModelResource):
    model_class = InvoiceItem


class InvoiceItemCollectionResource(ModelResource):
    model_class = InvoiceItem


# create meta resources
class InvoiceMeta(MetaResource):
    resource_class = InvoiceResource


class InvoiceMetaCollection(MetaResource):
    resource_class = InvoiceResource


class InvoiceItemMeta(MetaResource):
    resource_class = InvoiceItemResource


class InvoiceItemMetaCollection(MetaResource):
    resource_class = InvoiceItemResource


# add the resources to the API
api.add_resource(
    InvoiceCollectionResource, *InvoiceCollectionResource.get_urls()
)
api.add_resource(InvoiceResource, *InvoiceResource.get_urls())
api.add_resource(
    InvoiceItemCollectionResource, *InvoiceItemCollectionResource.get_urls()
)
api.add_resource(InvoiceItemResource, *InvoiceResource.get_urls())

api.add_resource(InvoiceMeta, *InvoiceMeta.get_urls())
api.add_resource(InvoiceMetaCollection, *InvoiceMetaCollection.get_urls())
api.add_resource(InvoiceItemMeta, *InvoiceItemMeta.get_urls())
api.add_resource(
    InvoiceItemMetaCollection, *InvoiceItemMetaCollection.get_urls()
)


if __name__ == "__main__":
    app.run(debug=True)
