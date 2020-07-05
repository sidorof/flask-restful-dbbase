.. code-block:: python 

    class User(db.Model):
        __tablename__ = "user"
    
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(80), unique=True, nullable=False)
        password = db.WriteOnlyColumn(db.String(80), nullable=False)
        is_staff = db.Column(db.Boolean, default=False, nullable=True)
        is_active = db.Column(db.Boolean, default=False, nullable=True)
        is_account_current = db.Column(db.Boolean, default=False, nullable=True)
    
        date_joined = db.Column(db.Date, default=date.today, nullable=True)
        last_login = db.Column(db.DateTime, nullable=True)
    
        SERIAL_FIELDS = ["username", "email"]
    
    
    db.create_all()
    
..