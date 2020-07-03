.. code-block:: python 

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
    
    
..