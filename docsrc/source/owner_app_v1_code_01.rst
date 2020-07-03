.. code-block:: python 

    class User(db.Model):
        __tablename__ = "user"
    
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        username = db.Column(db.String(80), nullable=False)
        password = db.WriteOnlyColumn(db.String(80), nullable=False)
        email = db.Column(db.String(80), unique=True, nullable=False)
    
        is_staff = db.Column(db.Boolean, default=False, nullable=False)
        is_active = db.Column(db.Boolean, default=False, nullable=False)
        is_account_current = db.Column(db.Boolean, default=False, nullable=False)
    
        date_joined = db.Column(db.Date, default=date.today, nullable=False)
        last_login = db.Column(db.DateTime, nullable=True)
    
    
..