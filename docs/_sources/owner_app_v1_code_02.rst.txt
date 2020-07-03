.. code-block:: python 

    class Order(db.Model):
        __tablename__ = "order"
    
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
        description = db.Column(db.String, nullable=False)
        ordered_at = db.Column(db.DateTime, default=datetime.now)
        status_id = db.Column(db.SmallInteger, default=0, nullable=True)
    
    
..