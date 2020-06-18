# examples/simple_app.py
"""
This app is a simple version showing usage of Flask-RESTful-DBBase.

Using the defaults and characteristics of the model tables,
resources can use those models to implement an API that has
the method GET/POST/PUT/PATCH/DELETE for single resources and
a GET for collection resources.

Serialization services convert JSON camel case variables into to
snake case more consistent with Python standards. Output data
is converted back to JSON camel case.

In addition, the meta resources can provide guidance to users
of the API for creating front-end applications.

Since Flask-RESTful provides method decorators, resources can
be protected on a table basis by method.

For simple data in / data out, such an approach can cover a
number of situations.

There are a number of simple modifications that can be applied to tweak
the resources and models for more complicated situations. Those
will be found in the documentation and other examples.
"""
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

author = Author(first_name="Geoffrey", last_name="Cooper").save()

book = Book(
    isbn="0-87893-214-3",
    title="The Cell: A Molecular Approach, 3rd edition",
    pub_year=2004,
    author_id=author.id,
).save()
book = Book(
    isbn="978-0878932191",
    title="The Cell: A Molecular Approach, 4th edition",
    pub_year=2006,
    author_id=author.id,
).save()

book = Book(
    isbn="978-1605352909",
    title="The Cell: A Molecular Approach, 7th edition",
    pub_year=2015,
    author_id=author.id,
).save()

book = Book(
    isbn="978-1605357072",
    title="The Cell: A Molecular Approach, 9th edition",
    pub_year=2018,
    author_id=author.id,
).save()

author = Author(first_name="Serope", last_name="Kalpakjian").save()

book = Book(
    isbn="978-0133128741",
    title="Manufacturing Engineering & Technology (7th Edition)",
    pub_year=2013,
    author_id=author.id,
).save()

author = Author(first_name="Steven", last_name="Skiena").save()


# api.create_resources(models=[Book, Author])`
class BookCollection(CollectionModelResource):
    model_class = Book
    url_name = "books"


class BookResource(ModelResource):
    model_class = Book
    url_name = "books"


class BookMetaCollection(MetaResource):
    resource_class = BookCollection


class BookMeta(MetaResource):
    resource_class = BookResource


class AuthorCollection(CollectionModelResource):
    model_class = Author
    url_name = "authors"


class AuthorResource(ModelResource):
    model_class = Author
    url_name = "authors"


class AuthorMetaCollection(MetaResource):
    resource_class = AuthorCollection


class AuthorMeta(MetaResource):
    resource_class = AuthorResource


print()
print("urls created:")
print("-------------")
print("\n".join(AuthorCollection.get_urls()))
print("\n".join(AuthorResource.get_urls()))
print()
print("\n".join(BookCollection.get_urls()))
print("\n".join(BookResource.get_urls()))
print()
print("\n".join(AuthorMeta.get_urls()))
print("\n".join(AuthorMetaCollection.get_urls()))
print("\n".join(BookMeta.get_urls()))
print("\n".join(BookMetaCollection.get_urls()))
print()

api.add_resource(AuthorCollection, *AuthorCollection.get_urls())
api.add_resource(AuthorResource, *AuthorResource.get_urls())
api.add_resource(AuthorMetaCollection, *AuthorMetaCollection.get_urls())
api.add_resource(AuthorMeta, *AuthorMeta.get_urls())

api.add_resource(BookCollection, *BookCollection.get_urls())
api.add_resource(BookResource, *BookResource.get_urls())
api.add_resource(BookMetaCollection, *BookMetaCollection.get_urls())
api.add_resource(BookMeta, *BookMeta.get_urls())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
