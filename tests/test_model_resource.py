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
    return True, item, status_code


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

    class DateTable(db.Model):
        __tablename__ = "test_dates"
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        today = db.Column(db.Date)
        now = db.Column(db.DateTime)

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

    return Author, Book, DateTable, author, book


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
            Author, Book, DateTable, author, book = create_models(db)
            cls.Author = Author
            cls.Book = Book
            cls.DateTable = DateTable
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

            # date conversions set to False to start
            class DateResource(ModelResource):
                model_class = DateTable
                use_date_conversions = False

            cls.api.add_resource(BookResource, *BookResource.get_urls())
            cls.api.add_resource(AuthorResource, *AuthorResource.get_urls())

            cls.api.add_resource(DateResource, *DateResource.get_urls())

            cls.needs_setup = False

            cls.BookResource = BookResource
            cls.AuthorResource = AuthorResource
            cls.DateResource = DateResource

        headers = {"Content-Type": "application/json"}
        cls.set_db = set_db
        cls.app = app
        cls.api = api
        cls.db = db
        cls.headers = headers

    @classmethod
    def tearDownClass(cls):
        cls.db.session.rollback()
        cls.db.session.remove()
        cls.db.drop_all()
        cls.db.Model.metadata.clear()
        cls.db = None
        del cls.db

    def test_model_name(self):

        db = self.db

        class TestModel(db.Model):
            __tablename__ = "test"
            id = db.Column(db.Integer, primary_key=True)

        class TestResource(ModelResource):
            pass

        self.assertRaises(ValueError, TestResource)
        TestResource.model_class = TestModel

        self.assertEqual(TestResource().model_name, "TestModel")

    def test_is_collection(self):

        self.assertFalse(self.BookResource.is_collection())

    def test_get_404(self):

        wrong_id = 10

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.get(f"/books/{wrong_id}", headers=self.headers)
            self.assertEqual(res.status_code, 404)
            self.assertDictEqual(
                res.get_json(), {"message": "Book with {'id': 10} not found"},
            )
            self.assertEqual(res.content_type, "application/json")

    def test_get(self):

        id = 1

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.get(f"/books/{id}", headers=self.headers)
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
                "/books", data=json.dumps(book), headers=self.headers
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
                "/books", data=json.dumps(book), headers=self.headers
            )
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": [
                        {"title": "The data exceeds the maximum length 100"},
                        {
                            "pub_year": "The value two "
                            "thousand 4 is not a number"
                        },
                        {"missing_columns": ["author_id"]},
                    ]
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post_bad_date_data(self):

        bad_datetbl = {"today": "wrong", "now": "wrong"}

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            # no date conversions
            res = client.post(
                "/date-tables",
                data=json.dumps(bad_datetbl),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "Internal Server Error: "
                    "method post: /date-tables"
                },
            )
            self.assertEqual(res.content_type, "application/json")

            # now set date conversions
            self.DateResource.use_date_conversions = True
            res = client.post(
                "/date-tables",
                data=json.dumps(bad_datetbl),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": [
                        {
                            "today": "Date error: 'wrong': Unknown string format: wrong"
                        },
                        {
                            "now": "Date error: 'wrong': Unknown string format: wrong"
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
                "/books", data=json.dumps(book), headers=self.headers
            )
            self.assertEqual(res.status_code, 409)
            self.assertDictEqual(
                res.get_json(),
                {"message": "{'id': 1} for Book already exists."},
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post(self):
        """Successful post, database assigns an id."""
        book = {
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 30th edition",
            "pub_year": 2034,
            # "author_id": 1,
        }

        author = {"first_name": "joe", "last_name": "fonebone", "books": book}

        # do it wrong first
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                "/authors", data=json.dumps(author), headers=self.headers
            )

            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {"message": "books data must be in a list form"},
            )

            # wrong because author is incomplete
            bad_book = {
                "isbn": "an isbn",
                "pub_year": "wrong",
            }
            author = {
                "first_name": "joe",
                "last_name": "fonebone",
                "books": [bad_book],
            }

            res = client.post(
                "/authors", data=json.dumps(author), headers=self.headers
            )

            self.assertEqual(res.status_code, 400)
            result = res.get_json()
            self.assertDictEqual(
                result,
                {"message": [{"pub_year": "The value wrong is not a number"}]},
            )
            author = {
                "first_name": "joe",
                "last_name": "fonebone",
                "books": [book],
            }

            res = client.post(
                "/authors", data=json.dumps(author), headers=self.headers
            )

            self.assertEqual(res.status_code, 201)
            result = res.get_json()

            self.assertDictEqual(
                result,
                {
                    "firstName": "joe",
                    "lastName": "fonebone",
                    "fullName": "joe fonebone",
                    "id": 2,
                    "books": [
                        {
                            "title": "The Cell: A Molecular Approach, "
                            "30th edition",
                            "pubYear": 2034,
                            "isbn": "an isbn",
                            "id": 1001,
                            "authorId": 2,
                        }
                    ],
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post_not_json(self):
        """not JSON"""
        book = {
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 30th edition",
            "pub_year": 2034,
            "author_id": 1,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            # incorrect json entry
            res = client.post(
                "/books", data=json.dumps(book)[:-1], headers=self.headers
            )
            self.assertEqual(res.status_code, 400)
            self.assertTrue(
                res.get_json()["message"].startswith(
                    "A JSON format problem:400 Bad Request: "
                )
            )

            self.assertEqual(res.content_type, "application/json")

    def test_post_not_json1(self):
        """
        not JSON, reject
        """
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.post(
                "/books", data='isbn="newisbn", title="new title"',
            )
            self.assertEqual(res.status_code, 415)
            self.assertDictEqual(
                res.get_json(), {"message": "JSON format is required"},
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
                "/books", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "This method requires the id in "
                    "the URL for Book."
                },
            )
            self.assertEqual(res.content_type, "application/json")

        with self.app.test_client() as client:
            res = client.patch("/books", headers=self.headers)
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "This method requires the id in "
                    "the URL for Book."
                },
            )
            self.assertEqual(res.content_type, "application/json")

        with self.app.test_client() as client:
            res = client.delete("/books", headers=self.headers)
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "This method requires the id in "
                    "the URL for Book."
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
                "/books/1", data=json.dumps(book), headers=self.headers
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
                "/books/1", data=json.dumps(book), headers=self.headers
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
                        {"missing_columns": ["author_id"]},
                    ]
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_put_not_json(self):
        """not JSON"""
        book = {
            "id": 1000,
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 30th edition",
            "pub_year": 2034,
            "author_id": 1,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            # incorrect json entry
            res = client.put(
                "/books/1000",
                data=json.dumps(book)[:-1],
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 400)
            self.assertTrue(
                res.get_json()["message"].startswith(
                    "A JSON format problem:400 Bad Request: "
                )
            )
            self.assertEqual(res.content_type, "application/json")

    def test_put_not_json1(self):
        """not JSON, reject"""

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.put(
                "/books/1000", data='isbn="newisbn", title="new title"',
            )
            self.assertEqual(res.status_code, 415)
            self.assertDictEqual(
                res.get_json(), {"message": "JSON format is required"},
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
                f"/books/{id}", data=json.dumps(book), headers=self.headers
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

    def test_patch_not_json(self):
        """not JSON"""
        book = {
            "id": 1000,
            "isbn": "an isbn",
            "title": "The Cell: A Molecular Approach, 30th edition",
            "pub_year": 2034,
            "author_id": 1,
        }
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            self.Book(**book).save()

            # incorrect json entry
            res = client.patch(
                "/books/1000",
                data=json.dumps(book)[:-1],
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 400)
            self.assertTrue(
                res.get_json()["message"].startswith(
                    "A JSON format problem:400 Bad Request: "
                )
            )

            self.assertEqual(res.content_type, "application/json")

    def test_patch_not_json1(self):
        """not JSON, reject
        """
        data = 'isbn="newisbnafsasfasfasdsdsdfsdsadasf", title="new title"'
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.patch("/books/1000", data=data,)
            self.assertEqual(res.status_code, 415)
            self.assertDictEqual(
                res.get_json(), {"message": "JSON format is required"},
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
                "/books/1", data=json.dumps(book), headers=self.headers
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
                f"/books/{id}", data=json.dumps(book), headers=self.headers
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
            res = client.delete(f"/books/{wrong_id}", headers=self.headers)
            self.assertEqual(res.status_code, 404)
            self.assertDictEqual(
                res.get_json(), {"message": "Book with {'id': 10} not found"},
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

            res = client.delete(f"/books/{book.id}", headers=self.headers)
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {"message": "Book with {} is deleted".format({"id": book.id})},
            )
            self.assertEqual(res.content_type, "application/json")

    def test_meta(self):

        self.assertDictEqual(
            self.BookResource.get_meta(),
            {
                "modelClass": "Book",
                "urlPrefix": "/",
                "baseUrl": "/books",
                "methods": {
                    "get": {
                        "url": "/books/<int:id>",
                        "input": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            }
                        },
                        "responses": [
                            {
                                "fields": {
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
                                                "firstName": {
                                                    "type": "string",
                                                    "maxLength": 50,
                                                    "nullable": False,
                                                    "info": {},
                                                },
                                                "lastName": {
                                                    "type": "string",
                                                    "maxLength": 50,
                                                    "nullable": False,
                                                    "info": {},
                                                },
                                                "fullName": {"readOnly": True},
                                            },
                                        },
                                    },
                                    "title": {
                                        "type": "string",
                                        "maxLength": 100,
                                        "nullable": False,
                                        "info": {},
                                    },
                                    "isbn": {
                                        "type": "string",
                                        "maxLength": 20,
                                        "nullable": True,
                                        "info": {},
                                    },
                                    "pubYear": {
                                        "type": "integer",
                                        "format": "int32",
                                        "nullable": False,
                                        "info": {},
                                    },
                                    "id": {
                                        "type": "integer",
                                        "format": "int32",
                                        "primary_key": True,
                                        "nullable": True,
                                        "info": {},
                                    },
                                    "authorId": {
                                        "type": "integer",
                                        "format": "int32",
                                        "nullable": False,
                                        "foreign_key": "author.id",
                                        "info": {},
                                    },
                                }
                            }
                        ],
                    },
                    "post": {
                        "url": "/books",
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
                        "responses": [
                            {
                                "fields": {
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
                                                "firstName": {
                                                    "type": "string",
                                                    "maxLength": 50,
                                                    "nullable": False,
                                                    "info": {},
                                                },
                                                "lastName": {
                                                    "type": "string",
                                                    "maxLength": 50,
                                                    "nullable": False,
                                                    "info": {},
                                                },
                                                "fullName": {"readOnly": True},
                                            },
                                        },
                                    },
                                    "title": {
                                        "type": "string",
                                        "maxLength": 100,
                                        "nullable": False,
                                        "info": {},
                                    },
                                    "isbn": {
                                        "type": "string",
                                        "maxLength": 20,
                                        "nullable": True,
                                        "info": {},
                                    },
                                    "pubYear": {
                                        "type": "integer",
                                        "format": "int32",
                                        "nullable": False,
                                        "info": {},
                                    },
                                    "id": {
                                        "type": "integer",
                                        "format": "int32",
                                        "primary_key": True,
                                        "nullable": True,
                                        "info": {},
                                    },
                                    "authorId": {
                                        "type": "integer",
                                        "format": "int32",
                                        "nullable": False,
                                        "foreign_key": "author.id",
                                        "info": {},
                                    },
                                }
                            }
                        ],
                    },
                    "put": {
                        "url": "/books/<int:id>",
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
                        "responses": [
                            {
                                "fields": {
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
                                                "firstName": {
                                                    "type": "string",
                                                    "maxLength": 50,
                                                    "nullable": False,
                                                    "info": {},
                                                },
                                                "lastName": {
                                                    "type": "string",
                                                    "maxLength": 50,
                                                    "nullable": False,
                                                    "info": {},
                                                },
                                                "fullName": {"readOnly": True},
                                            },
                                        },
                                    },
                                    "title": {
                                        "type": "string",
                                        "maxLength": 100,
                                        "nullable": False,
                                        "info": {},
                                    },
                                    "isbn": {
                                        "type": "string",
                                        "maxLength": 20,
                                        "nullable": True,
                                        "info": {},
                                    },
                                    "pubYear": {
                                        "type": "integer",
                                        "format": "int32",
                                        "nullable": False,
                                        "info": {},
                                    },
                                    "id": {
                                        "type": "integer",
                                        "format": "int32",
                                        "primary_key": True,
                                        "nullable": True,
                                        "info": {},
                                    },
                                    "authorId": {
                                        "type": "integer",
                                        "format": "int32",
                                        "nullable": False,
                                        "foreign_key": "author.id",
                                        "info": {},
                                    },
                                }
                            }
                        ],
                    },
                    "patch": {
                        "url": "/books/<int:id>",
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
                        "responses": [
                            {
                                "fields": {
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
                                                "firstName": {
                                                    "type": "string",
                                                    "maxLength": 50,
                                                    "nullable": False,
                                                    "info": {},
                                                },
                                                "lastName": {
                                                    "type": "string",
                                                    "maxLength": 50,
                                                    "nullable": False,
                                                    "info": {},
                                                },
                                                "fullName": {"readOnly": True},
                                            },
                                        },
                                    },
                                    "title": {
                                        "type": "string",
                                        "maxLength": 100,
                                        "nullable": False,
                                        "info": {},
                                    },
                                    "isbn": {
                                        "type": "string",
                                        "maxLength": 20,
                                        "nullable": True,
                                        "info": {},
                                    },
                                    "pubYear": {
                                        "type": "integer",
                                        "format": "int32",
                                        "nullable": False,
                                        "info": {},
                                    },
                                    "id": {
                                        "type": "integer",
                                        "format": "int32",
                                        "primary_key": True,
                                        "nullable": True,
                                        "info": {},
                                    },
                                    "authorId": {
                                        "type": "integer",
                                        "format": "int32",
                                        "nullable": False,
                                        "foreign_key": "author.id",
                                        "info": {},
                                    },
                                }
                            }
                        ],
                    },
                    "delete": {
                        "url": "/books/<int:id>",
                        "input": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            }
                        },
                        "responses": [{}],
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

        def delete_before_commit(self, item, status_code):

            item = None
            return item, status_code

        class ThrowAwayResource(ModelResource):
            model_class = ThrowAway

            before_commit = {"delete": delete_before_commit}

        self.api.add_resource(ThrowAwayResource, *ThrowAwayResource.get_urls())

        with self.app.test_client() as client:
            self.db.drop_all()
            res = client.get("/throw-aways/1", headers=self.headers)

            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "Internal Server Error: "
                    "method get: /throw-aways/1"
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post_with_bad_db(self):
        """Uses a cheap trick by changing the item"""
        db = self.db

        class ThrowAwayPost(db.Model):
            __tablename__ = "throwaway_post"
            id = db.Column(db.Integer, nullable=True, primary_key=True)
            name = db.Column(db.String(50), nullable=False)

            def save(self):
                raise ValueError("trigger erroor")

        self.db.create_all()

        class ThrowAwayResource(ModelResource):
            model_class = ThrowAwayPost

            def process_post_input(self, data):
                self.model_class.query.first = "bad"

                return True, data

        self.ThrowAwayResource = ThrowAwayResource
        self.api.add_resource(ThrowAwayResource, *ThrowAwayResource.get_urls())

        with self.app.test_client() as client:
            item = dict(name="test")
            self.db.drop_all()

            res = client.post(
                "/throw-away-posts",
                data=json.dumps(item),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "Internal Server Error: method "
                    "post: /throw-away-posts"
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_put_with_bad_db(self):
        """Uses a cheap trick by changing the item"""
        db = self.db

        class ThrowAwayPut(db.Model):
            __tablename__ = "throwaway_put"
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50), nullable=False)

        self.db.create_all()

        def delete_before_commit(self, item, status_code):

            item = None
            return True, item, status_code

        class ThrowAwayResource(ModelResource):
            model_class = ThrowAwayPut

            def process_put_input(self, query, data, kwargs):
                """wreck the first function"""
                if "disrupt" in data:
                    query.first = "bad"
                    data.pop("disrupt")
                return True, (query, data)

            before_commit = {"put": delete_before_commit}

        self.ThrowAwayResource = ThrowAwayResource
        self.api.add_resource(ThrowAwayResource, *ThrowAwayResource.get_urls())

        with self.app.test_client() as client:
            item = ThrowAwayPut(name="test").save()

            res = client.put(
                f"/throw-away-puts/{item.id}",
                data=item.serialize(),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "An error occurred updating the "
                    "ThrowAwayPut: 'NoneType' object has no attribute "
                    "'save'."
                },
            )
            self.assertEqual(res.content_type, "application/json")

        with self.app.test_client() as client:
            item = ThrowAwayPut(name="test").save()
            data = item.to_dict()
            data["disrupt"] = True
            res = client.put(
                f"/throw-away-puts/{item.id}",
                data=json.dumps(data),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "Internal Server Error: method put: "
                    f"/throw-away-puts/{item.id}"
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_patch_with_bad_db(self):
        """Uses a cheap trick by changing the item"""
        db = self.db

        class ThrowAwayPatch(db.Model):
            __tablename__ = "throwaway_patch"
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50), nullable=False)

        self.db.create_all()

        def delete_before_commit(self, item, status_code):

            item = None
            return True, item, status_code

        class ThrowAwayResource(ModelResource):
            model_class = ThrowAwayPatch

            before_commit = {"patch": delete_before_commit}

        self.api.add_resource(ThrowAwayResource, *ThrowAwayResource.get_urls())

        with self.app.test_client() as client:
            item = ThrowAwayPatch(name="test").save()

            res = client.patch(
                f"/throw-away-patches/{item.id}",
                data=item.serialize(),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "An error occurred updating the "
                    "ThrowAwayPatch: 'NoneType' object has no attribute "
                    "'save'."
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_delete_with_bad_db(self):
        """Uses a cheap trick by changing the item"""
        db = self.db

        class ThrowAwayDelete(db.Model):
            __tablename__ = "throwaway_delete"
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50), nullable=False)

        self.db.create_all()

        def delete_before_commit(self, item, status_code):

            item = None
            return True, item, status_code

        class ThrowAwayResource(ModelResource):
            model_class = ThrowAwayDelete
            test = None

            def process_delete_input(self, query, kwargs):
                if self.test:
                    query.first = "bad"

                return True, query

            before_commit = {"delete": delete_before_commit}

        self.api.add_resource(ThrowAwayResource, *ThrowAwayResource.get_urls())

        self.ThrowAwayResource = ThrowAwayResource

        with self.app.test_client() as client:

            item = ThrowAwayDelete(name="test").save()

            res = client.delete(
                f"/throw-away-deletes/{item.id}", headers=self.headers
            )
            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "An error occurred deleting the "
                    "ThrowAwayDelete: 'NoneType' object has no attribute "
                    "'delete'."
                },
            )
            self.assertEqual(res.content_type, "application/json")

        with self.app.test_client() as client:
            self.ThrowAwayResource.test = True
            item = ThrowAwayDelete(name="test").save()

            res = client.delete(
                f"/throw-away-deletes/{item.id}", headers=self.headers
            )
            self.assertEqual(res.status_code, 500)
            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "Internal Server Error: method "
                    f"delete: /throw-away-deletes/{item.id}: 'str' object "
                    "is not callable"
                },
            )
            self.assertEqual(res.content_type, "application/json")
