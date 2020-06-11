# app.py
from flask import Flask
from flask_restful import Api
from flask_restful_dbbase import DBBase

app = Flask(__name__)
api = Api(app)
db = DBBase(app)

from flask_restful_dbbase.resources import (
    CollectionModelResource,
    ModelResource,
)


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    other = db.Column(db.String(), nullable=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    books = db.relationship("Book", backref="author", lazy="joined")


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    isbn = db.Column(db.String(20), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    pub_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("authors.id"), nullable=False
    )


db.create_all()

author = Author(
    first_name="Geoffrey", last_name="Cooper", other="something"
).save()

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

root_prefix = "/"

# api.create_resources(models=[Book, Author])`
class BookCollection(CollectionModelResource):
    model_class = Book
    url_prefix = root_prefix
    url_path = "books"


print(BookCollection.get_urls())


class BookResource(ModelResource):
    model_class = Book
    url_prefix = root_prefix
    url_path = "books"


class AuthorResource(ModelResource):
    model_class = Author
    url_prefix = root_prefix
    url_path = "authors"


print(*AuthorResource.get_urls())
print(*BookCollection.get_urls())
print(*BookResource.get_urls())

api.add_resource(AuthorResource, *AuthorResource.get_urls())
api.add_resource(BookCollection, *BookCollection.get_urls())
api.add_resource(BookResource, *BookResource.get_urls())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
