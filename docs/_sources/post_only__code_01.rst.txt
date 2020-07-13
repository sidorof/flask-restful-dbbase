.. code-block:: python 

    class AModel(db.Model):
        __tablename__ = "amodel"
    
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        description = db.Column(db.String(80), unique=True, nullable=False)
        num_variable = db.Column(db.Integer, nullable=False)
    
    
    db.create_all()
    
    
..