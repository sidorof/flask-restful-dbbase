.. code-block:: python 

    class Job(db.Model):
        __tablename__ = "job"
    
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        owner_id = db.Column(
            db.Integer, db.ForeignKey("user.id"), nullable=False)
        order_id = db.Column(
            db.Integer, db.ForeignKey("order.id"), nullable=False)
        started_at = db.Column(
            db.DateTime, server_default=db.func.now(), nullable=False
        )
        finished_at = db.Column(db.DateTime)
        status_id = db.Column(db.SmallInteger, default=0, nullable=True)
    
    
    db.create_all()
..