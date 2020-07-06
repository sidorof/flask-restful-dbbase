.. code-block:: python 

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
    
    
    class Author(db.Model):
        __tablename__ = "author"
    
        id = db.Column(db.Integer, primary_key=True, nullable=True)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
    
        def full_name(self):
            return f"{self.first_name} {self.last_name}"
    
        books = db.relationship("Book", backref="author", lazy="joined")
    
    
    class Book(db.Model):
        __tablename__ = "book"
    
        id = db.Column(db.Integer, primary_key=True, nullable=True)
        isbn = db.Column(db.String(20), nullable=True)
        title = db.Column(db.String(100), nullable=False)
        pub_year = db.Column(db.Integer, nullable=False)
        author_id = db.Column(
            db.Integer, db.ForeignKey("author.id"), nullable=False
        )
    
    
    db.create_all()
    
..