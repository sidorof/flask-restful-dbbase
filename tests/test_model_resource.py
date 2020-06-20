# tests/test_model_resource.py
import unittest
import logging
import json

import flask
import flask_restful
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import ModelResource

logging.disable(logging.CRITICAL)


def passthrough(self, item, status_code):
    """ passthrough

    For testing before/after commit functions
    """
    return item, status_code


def create_models(db):
    """create some sample models and a few records"""

    class Author(db.Model):
        __tablename__ = "author"

        id = db.Column(db.Integer, nullable=True, primary_key=True)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)

        def full_name(self):
            return f"{self.first_name} {self.last_name}"

        books = db.relationship("Book", backref="author", lazy="joined")

    class Book(db.Model):
        __tablename__ = "book"

        id = db.Column(db.Integer, nullable=True, primary_key=True)
        isbn = db.Column(db.String(20), nullable=True)
        title = db.Column(db.String(100), nullable=False)
        pub_year = db.Column(db.Integer, nullable=False)
        author_id = db.Column(
            db.Integer, db.ForeignKey("author.id"), nullable=False
        )

    db.create_all()

    # sample data
    author = Author(first_name="Geoffrey", last_name="Cooper").save()
    book = Book(
        isbn="0-87893-214-3",
        title="The Cell: A Molecular Approach, 3rd edition",
        pub_year=2004,
        author_id=author.id,
    )
    book.save()

    return Author, Book, author, book


class TestModelResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This doesn't check defaults.'
        """
        app = flask.Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        api = flask_restful.Api(app)
        db = DBBase(app)
        cls.needs_setup = True

        @classmethod
        def set_db(cls):
            Author, Book, author, book = create_models(db)
            cls.Author = Author
            cls.Book = Book
            cls.author = author
            cls.book = book

            class BookResource(ModelResource):
                model_class = cls.Book
                before_commit = {
                    "post": passthrough,
                    "put": passthrough,
                    "patch": passthrough,
                    "delete": passthrough,
                }

                after_commit = {
                    "post": passthrough,
                    "put": passthrough,
                    "patch": passthrough,
                }

            class AuthorResource(ModelResource):
                model_class = cls.Author

            cls.api.add_resource(BookResource, *BookResource.get_urls())
            cls.api.add_resource(AuthorResource, *AuthorResource.get_urls())
            cls.needs_setup = False

            cls.BookResource = BookResource
            cls.AuthorResource = AuthorResource

        headers = {"Content-Type": "application/json"}
        cls.set_db = set_db
        cls.app = app
        cls.api = api
        cls.db = db
        cls.headers = headers

    @classmethod
    def tearDownClass(cls):
        cls.db.session.commit()
        cls.db.session.close()
        cls.Author = None
        cls.Book = None
        cls.author = None
        cls.book = None

        cls.db.drop_all()
        cls.db.Model.metadata.clear()
        cls.db = None
        del cls.db

    def test_is_collection(self):

        self.assertFalse(self.BookResource.is_collection())

    def test_get_404(self):

        wrong_id = 10

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.get(f"/book/{wrong_id}", headers=self.headers)
            self.assertEqual(res.status_code, 404)
            self.assertDictEqual(
                res.get_json(), {"message": "Book with id of 10 not found"},
            )
            self.assertEqual(res.content_type, "application/json")

    def test_get(self):

        id = 1

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.get(f"/book/{id}", headers=self.headers)
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {
                    "title": "The Cell: A Molecular Approach, 3rd edition",
                    "pubYear": 2004,
                    "isbn": "0-87893-214-3",
                    "authorId": 1,
                    "id": 1,
                    "author": {
                        "lastName": "Cooper",
                        "firstName": "Geoffrey",
                        "id": 1,
                        "fullName": "Geoffrey Cooper",
                    },
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post_incomplete(self):

        book = {
            "isbn": "an isbn",
            # "title": "The Cell: A Molecular Approach, 3rd edition",
            # "pub_year": 2004,
            # "author_id": author.id,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.post(
                f"/book", data=json.dumps(book), headers=self.headers
            )

            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": [
                        {"missing_columns": ["title", "pub_year", "author_id"]}
                    ]
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post_bad_data(self):
        book = {
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 3rd edition" * 100,
            "pub_year": "two thousand 4",
            # "author_id": author.id,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.post(
                f"/book", data=json.dumps(book), headers=self.headers
            )
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": [
                        {"missing_columns": ["author_id"]},
                        {"title": "The data exceeds the maximum length 100"},
                        {
                            "pub_year": "The value two "
                            "thousand 4 is not a number"
                        },
                    ]
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post_existing_id(self):

        book = {
            "id": 1,
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 3rd edition",
            "pub_year": 2004,
            "author_id": 1,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.post(
                f"/book", data=json.dumps(book), headers=self.headers
            )
            self.assertEqual(res.status_code, 409)
            self.assertDictEqual(
                res.get_json(), {"message": "1 for Book already exists."}
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post(self):
        """Successful post, database assigns an id."""
        book = {
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 30th edition",
            "pub_year": 2034,
            "author_id": 1,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.post(
                f"/book", data=json.dumps(book), headers=self.headers
            )
            self.assertEqual(res.status_code, 201)
            self.assertDictEqual(
                res.get_json(),
                {
                    "pubYear": 2034,
                    "isbn": "an isbn",
                    "id": 2,
                    "title": "The Cell: A Molecular Approach, 30th edition",
                    "author": {
                        "firstName": "Geoffrey",
                        "lastName": "Cooper",
                        "id": 1,
                        "fullName": "Geoffrey Cooper",
                    },
                    "authorId": 1,
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_bad_url(self):
        """test_bad_url

        This test evaluates error generation for put/
        delete/patch when the key is not used.
        """
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.put(
                f"/book", data=json.dumps({}), headers=self.headers
            )

            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "No key for Book given. "
                    "This is a configuration problem in "
                    "the url for this kind of method."
                },
            )
            self.assertEqual(res.content_type, "application/json")

        with self.app.test_client() as client:
            res = client.patch(f"/book", headers=self.headers)
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "No key for Book given. "
                    "This is a configuration problem in "
                    "the url for this kind of method."
                },
            )
            self.assertEqual(res.content_type, "application/json")

        with self.app.test_client() as client:
            res = client.delete(f"/book", headers=self.headers)
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "No key for Book given. "
                    "This is a configuration problem in "
                    "the url for this kind of method."
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_put_incomplete(self):
        book = {
            "isbn": "an isbn",
            # "title": "The Cell: A Molecular Approach, 3rd edition",
            # "pub_year": 2004,
            # "author_id": author.id,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.put(
                f"/book/1", data=json.dumps(book), headers=self.headers
            )

            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": [
                        {"missing_columns": ["title", "pub_year", "author_id"]}
                    ]
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_put_bad_data(self):
        book = {
            "id": 1,
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 3rd edition" * 100,
            "pub_year": "two thousand 4",
            # "author_id": author.id,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.put(
                f"/book/1", data=json.dumps(book), headers=self.headers
            )
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": [
                        {"missing_columns": ["author_id"]},
                        {"title": "The data exceeds the maximum length 100"},
                        {
                            "pub_year": "The value two "
                            "thousand 4 is not a number"
                        },
                    ]
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_put(self):

        book = {
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 3rd edition",
            "pub_year": 2004,
            "author_id": 1,
        }
        id = 1
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.put(
                f"/book/{id}", data=json.dumps(book), headers=self.headers
            )
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {
                    "title": "The Cell: A Molecular Approach, 3rd edition",
                    "id": 1,
                    "isbn": "an isbn",
                    "authorId": 1,
                    "pubYear": 2004,
                    "author": {
                        "id": 1,
                        "fullName": "Geoffrey Cooper",
                        "firstName": "Geoffrey",
                        "lastName": "Cooper",
                    },
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_patch_bad_data(self):
        book = {
            "id": 1,
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 3rd edition" * 100,
            "pub_year": "two thousand 4",
            # "author_id": author.id,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.patch(
                f"/book/1", data=json.dumps(book), headers=self.headers
            )

            self.assertDictEqual(
                res.get_json(),
                {
                    "message": [
                        {"title": "The data exceeds the maximum length 100"},
                        {
                            "pub_year": "The value two "
                            "thousand 4 is not a number"
                        },
                    ]
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_patch(self):
        # just change the title
        book = {
            # "isbn": "0-87893-214-3",
            "title": "The New Title",
            # "pub_year": 2004,
            # "author_id": 1,
        }
        id = 1
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.patch(
                f"/book/{id}", data=json.dumps(book), headers=self.headers
            )
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {
                    "title": "The New Title",
                    "id": 1,
                    "isbn": "0-87893-214-3",
                    "authorId": 1,
                    "pubYear": 2004,
                    "author": {
                        "id": 1,
                        "fullName": "Geoffrey Cooper",
                        "firstName": "Geoffrey",
                        "lastName": "Cooper",
                    },
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_delete_404(self):

        wrong_id = 10

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.delete(f"/book/{wrong_id}", headers=self.headers)
            self.assertEqual(res.status_code, 404)
            self.assertDictEqual(
                res.get_json(), {"message": "Book with id of 10 not found"},
            )
            self.assertEqual(res.content_type, "application/json")

    def test_delete(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            # create a book
            book = self.Book(
                isbn="0-12345-214-3",
                title="The Big Red Book of Deletions",
                pub_year=2020,
                author_id=1,
            ).save()

            res = client.delete(f"/book/{book.id}", headers=self.headers)
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {"message": f"Book with id of {book.id} is deleted"},
            )
            self.assertEqual(res.content_type, "application/json")

    def test_meta(self):

        self.assertDictEqual(
            self.BookResource.get_meta(),
            {
                "model_class": "Book",
                "url_prefix": "/",
                "url": "/book",
                "methods": {
                    "get": {
                        "url": "/book/<int:id>",
                        "requirements": [],
                        "input": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            }
                        },
                        "responses": {
                            "fields": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "isbn": {
                                    "type": "string",
                                    "maxLength": 20,
                                    "nullable": True,
                                    "info": {},
                                },
                                "title": {
                                    "type": "string",
                                    "maxLength": 100,
                                    "nullable": False,
                                    "info": {},
                                },
                                "pub_year": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "author_id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "foreign_key": "author.id",
                                    "info": {},
                                },
                                "author": {
                                    "readOnly": True,
                                    "relationship": {
                                        "type": "single",
                                        "entity": "Author",
                                        "fields": {
                                            "id": {
                                                "type": "integer",
                                                "format": "int32",
                                                "primary_key": True,
                                                "nullable": True,
                                                "info": {},
                                            },
                                            "first_name": {
                                                "type": "string",
                                                "maxLength": 50,
                                                "nullable": False,
                                                "info": {},
                                            },
                                            "last_name": {
                                                "type": "string",
                                                "maxLength": 50,
                                                "nullable": False,
                                                "info": {},
                                            },
                                            "full_name": {"readOnly": True},
                                        },
                                    },
                                },
                            }
                        },
                    },
                    "post": {
                        "requirements": [],
                        "input": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            },
                            "isbn": {
                                "type": "string",
                                "maxLength": 20,
                                "nullable": True,
                                "info": {},
                            },
                            "title": {
                                "type": "string",
                                "maxLength": 100,
                                "nullable": False,
                                "info": {},
                            },
                            "pubYear": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "info": {},
                            },
                            "authorId": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "foreign_key": "author.id",
                                "info": {},
                            },
                        },
                        "responses": {
                            "fields": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "isbn": {
                                    "type": "string",
                                    "maxLength": 20,
                                    "nullable": True,
                                    "info": {},
                                },
                                "title": {
                                    "type": "string",
                                    "maxLength": 100,
                                    "nullable": False,
                                    "info": {},
                                },
                                "pub_year": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "author_id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "foreign_key": "author.id",
                                    "info": {},
                                },
                                "author": {
                                    "readOnly": True,
                                    "relationship": {
                                        "type": "single",
                                        "entity": "Author",
                                        "fields": {
                                            "id": {
                                                "type": "integer",
                                                "format": "int32",
                                                "primary_key": True,
                                                "nullable": True,
                                                "info": {},
                                            },
                                            "first_name": {
                                                "type": "string",
                                                "maxLength": 50,
                                                "nullable": False,
                                                "info": {},
                                            },
                                            "last_name": {
                                                "type": "string",
                                                "maxLength": 50,
                                                "nullable": False,
                                                "info": {},
                                            },
                                            "full_name": {"readOnly": True},
                                        },
                                    },
                                },
                            }
                        },
                    },
                    "put": {
                        "url": "/book/<int:id>",
                        "requirements": [],
                        "input": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            },
                            "isbn": {
                                "type": "string",
                                "maxLength": 20,
                                "nullable": True,
                                "info": {},
                            },
                            "title": {
                                "type": "string",
                                "maxLength": 100,
                                "nullable": False,
                                "info": {},
                            },
                            "pubYear": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "info": {},
                            },
                            "authorId": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "foreign_key": "author.id",
                                "info": {},
                            },
                        },
                        "responses": {
                            "fields": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "isbn": {
                                    "type": "string",
                                    "maxLength": 20,
                                    "nullable": True,
                                    "info": {},
                                },
                                "title": {
                                    "type": "string",
                                    "maxLength": 100,
                                    "nullable": False,
                                    "info": {},
                                },
                                "pub_year": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "author_id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "foreign_key": "author.id",
                                    "info": {},
                                },
                                "author": {
                                    "readOnly": True,
                                    "relationship": {
                                        "type": "single",
                                        "entity": "Author",
                                        "fields": {
                                            "id": {
                                                "type": "integer",
                                                "format": "int32",
                                                "primary_key": True,
                                                "nullable": True,
                                                "info": {},
                                            },
                                            "first_name": {
                                                "type": "string",
                                                "maxLength": 50,
                                                "nullable": False,
                                                "info": {},
                                            },
                                            "last_name": {
                                                "type": "string",
                                                "maxLength": 50,
                                                "nullable": False,
                                                "info": {},
                                            },
                                            "full_name": {"readOnly": True},
                                        },
                                    },
                                },
                            }
                        },
                    },
                    "patch": {
                        "url": "/book/<int:id>",
                        "requirements": [],
                        "input": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            },
                            "isbn": {
                                "type": "string",
                                "maxLength": 20,
                                "nullable": True,
                                "info": {},
                            },
                            "title": {
                                "type": "string",
                                "maxLength": 100,
                                "nullable": False,
                                "info": {},
                            },
                            "pubYear": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "info": {},
                            },
                            "authorId": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "foreign_key": "author.id",
                                "info": {},
                            },
                        },
                        "responses": {
                            "fields": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "isbn": {
                                    "type": "string",
                                    "maxLength": 20,
                                    "nullable": True,
                                    "info": {},
                                },
                                "title": {
                                    "type": "string",
                                    "maxLength": 100,
                                    "nullable": False,
                                    "info": {},
                                },
                                "pub_year": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "author_id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "foreign_key": "author.id",
                                    "info": {},
                                },
                                "author": {
                                    "readOnly": True,
                                    "relationship": {
                                        "type": "single",
                                        "entity": "Author",
                                        "fields": {
                                            "id": {
                                                "type": "integer",
                                                "format": "int32",
                                                "primary_key": True,
                                                "nullable": True,
                                                "info": {},
                                            },
                                            "first_name": {
                                                "type": "string",
                                                "maxLength": 50,
                                                "nullable": False,
                                                "info": {},
                                            },
                                            "last_name": {
                                                "type": "string",
                                                "maxLength": 50,
                                                "nullable": False,
                                                "info": {},
                                            },
                                            "full_name": {"readOnly": True},
                                        },
                                    },
                                },
                            }
                        },
                    },
                    "delete": {
                        "url": "/book/<int:id>",
                        "requirements": [],
                        "input": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            }
                        },
                        "responses": {},
                    },
                },
                "table": {
                    "Book": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            },
                            "isbn": {
                                "type": "string",
                                "maxLength": 20,
                                "nullable": True,
                                "info": {},
                            },
                            "title": {
                                "type": "string",
                                "maxLength": 100,
                                "nullable": False,
                                "info": {},
                            },
                            "pub_year": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "info": {},
                            },
                            "author_id": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "foreign_key": "author.id",
                                "info": {},
                            },
                            "author": {
                                "readOnly": True,
                                "relationship": {
                                    "type": "single",
                                    "entity": "Author",
                                    "fields": {
                                        "id": {
                                            "type": "integer",
                                            "format": "int32",
                                            "primary_key": True,
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "first_name": {
                                            "type": "string",
                                            "maxLength": 50,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "last_name": {
                                            "type": "string",
                                            "maxLength": 50,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "full_name": {"readOnly": True},
                                    },
                                },
                            },
                        },
                        "xml": "Book",
                    }
                },
            },
        )


class TestModelBadDatabase(unittest.TestCase):
    def setUp(self):
        """
        This doesn't check defaults.'
        """
        app = flask.Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        api = flask_restful.Api(app)
        db = DBBase(app)
        headers = {"Content-Type": "application/json"}

        self.app = app
        self.api = api
        self.db = db
        self.headers = headers

    def test_get_with_bad_db(self):

        db = self.db

        class ThrowAway(db.Model):
            __tablename__ = "throwaway"
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50), nullable=False)

        self.db.create_all()

        class ThrowAwayResource(ModelResource):
            model_class = ThrowAway

        self.api.add_resource(ThrowAwayResource, *ThrowAwayResource.get_urls())

        with self.app.test_client() as client:
            self.db.drop_all()
            res = client.get(f"/throw-away/1", headers=self.headers)

            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "Internal Server Error: "
                    "method get: /throw-away/1"
                },
            )
            self.assertEqual(res.content_type, "application/json")
