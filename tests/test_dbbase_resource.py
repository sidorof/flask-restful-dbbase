# tests/test_dbbase_resource.py
import pytest
from dbbase import DB
from flask_restful_dbbase.resources import DBBaseResource

from .models.user_address import User, Address


def create_models(db):
    class Author(db.Model):
        __tablename__ = "author"

        id = db.Column(db.Integer, primary_key=True)
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


def test_default_class_variables():

    assert DBBaseResource.model_class is None
    assert DBBaseResource.model_class is None
    assert DBBaseResource.url_prefix == "/"
    assert DBBaseResource.url_name is None

    assert DBBaseResource.serial_fields is None
    assert DBBaseResource.serial_field_relations is None

    assert DBBaseResource.default_sort is None
    assert DBBaseResource.requires_parameter is False
    assert DBBaseResource.fields is None


def test_get_key():
    class UserResource(DBBaseResource):
        model_class = User

    assert UserResource.get_key(formatted=False) == "username"
    assert UserResource.get_key(formatted=True) == "<string:username>"

    class AddressResource(DBBaseResource):
        model_class = Address

    assert AddressResource.get_key(formatted=False) == "id"
    assert AddressResource.get_key(formatted=True) == "<int:id>"


def test_get_obj_params():
    class UserResource(DBBaseResource):
        model_class = User

    obj_params = UserResource.get_obj_params()

    assert UserResource.get_obj_params() == {
        "username": {
            "type": "string",
            "maxLength": 80,
            "primary_key": True,
            "nullable": False,
            "info": {},
        },
        "password": {
            "type": "string",
            "maxLength": 80,
            "nullable": False,
            "info": {"write-only": True},
        },
        "email": {
            "type": "string",
            "maxLength": 80,
            "nullable": False,
            "unique": True,
            "info": {},
        },
        "first_name": {
            "type": "string",
            "maxLength": 80,
            "nullable": True,
            "info": {},
        },
        "last_name": {
            "type": "string",
            "maxLength": 80,
            "nullable": True,
            "info": {},
        },
        "company": {
            "type": "string",
            "maxLength": 255,
            "nullable": True,
            "info": {},
        },
        "is_superuser": {
            "type": "boolean",
            "nullable": False,
            "default": {"for_update": False, "arg": False},
            "info": {},
        },
        "is_staff": {
            "type": "boolean",
            "nullable": False,
            "default": {"for_update": False, "arg": False},
            "info": {},
        },
        "is_active": {
            "type": "boolean",
            "nullable": False,
            "default": {"for_update": False, "arg": False},
            "info": {},
        },
        "is_account_current": {
            "type": "boolean",
            "nullable": False,
            "default": {"for_update": False, "arg": False},
            "info": {},
        },
        "date_joined": {
            "type": "date",
            "nullable": False,
            "default": {"for_update": False, "arg": "date.today"},
            "info": {},
        },
        "last_login": {"type": "date-time", "nullable": True, "info": {}},
        "addresses": {
            "readOnly": True,
            "relationship": {
                "type": "list",
                "entity": "Address",
                "fields": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": True,
                        "nullable": False,
                        "info": {},
                    },
                    "email_address": {
                        "type": "string",
                        "nullable": False,
                        "info": {},
                    },
                    "username": {
                        "type": "string",
                        "nullable": True,
                        "foreign_key": "user.username",
                        "info": {},
                    },
                },
            },
        },
    }


def test_format_key():

    key = "test"
    key_type = "integer"

    assert DBBaseResource.format_key(key, key_type) == "<int:test>"

    key_type = "string"

    assert DBBaseResource.format_key(key, key_type) == "<string:test>"


def test_get_urls():
    class UserResource(DBBaseResource):
        model_class = User

    urls = UserResource.get_urls()

    assert urls == ["/user", "/user/<string:username>"]

    UserResource.url_prefix = "/api/v1"
    UserResource.url_name = "users"

    urls = UserResource.get_urls()

    assert urls == ["/api/v1/users", "/api/v1/users/<string:username>"]

    class TestResource(DBBaseResource):
        pass

    assert TestResource.model_class is None

    with pytest.raises(ValueError) as err:
        TestResource.get_urls()
    assert str(err.value) == "A model class must be defined"

    # multiple keys
    db = DB(config=":memory:")

    class MultKeys(db.Model):
        __tablename__ = "mult_keys"
        key1 = db.Column(db.String, primary_key=True)
        key2 = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)

    db.create_all()

    class MultKeyResource(DBBaseResource):
        model_class = MultKeys

    assert MultKeyResource.get_urls() == [
        "/mult-keys",
        "/mult-keys/<string:key1><int:key2>",
    ]


def test__check_key():
    class UserResource(DBBaseResource):
        model_class = User

    kwargs = {"username": "test"}

    # finds the key
    assert UserResource._check_key(kwargs) == ("username", "test")

    kwargs = {"something": "else"}

    # does not find the key
    pytest.raises(ValueError, UserResource._check_key, kwargs)


def test__get_serial_fields():
    class UserResource(DBBaseResource):
        model_class = User

    # nothing special for methods
    assert UserResource._get_serial_fields(method="something") is None

    UserResource.serial_fields = {
        "get": ["username", "company", "email"],
        "post": [
            "date_joined",
            "addresses",
            "last_login",
            "is_active",
            "is_account_current",
            "is_superuser",
            "username",
            "email",
            "company",
            "password",
            "last_name",
            "first_name",
            "is_staff",
        ],
        "patch": ["email"],
    }

    assert UserResource._get_serial_fields(method="get") == [
        "username",
        "company",
        "email",
    ]

    assert UserResource._get_serial_fields(method="post") == [
        "date_joined",
        "addresses",
        "last_login",
        "is_active",
        "is_account_current",
        "is_superuser",
        "username",
        "email",
        "company",
        "password",
        "last_name",
        "first_name",
        "is_staff",
    ]

    assert UserResource._get_serial_fields(method="patch") == ["email"]

    # unspecified for particular method, but still a dict
    assert UserResource._get_serial_fields(method="put") is None


def test__get_serial_field_relations():
    class UserResource(DBBaseResource):
        model_class = User

    User.SERIAL_FIELD_RELATIONS = {"Address": ["city", "state"]}

    assert UserResource._get_serial_field_relations(method="get") == {
        "Address": ["city", "state"]
    }

    UserResource.serial_field_relations = {
        "get": {"Address": ["city"]},
        "post": {"Address": ["city", "state", "company"]},
    }

    assert UserResource._get_serial_field_relations("get") == {
        "Address": ["city"]
    }

    assert UserResource._get_serial_field_relations("post") == {
        "Address": ["city", "state", "company"]
    }

    assert UserResource._get_serial_field_relations("other") == {
        "Address": ["city", "state"]
    }


def test__get_serializations():
    class UserResource(DBBaseResource):
        model_class = User

    UserResource.serial_fields = {
        "get": ["username", "company", "email"],
        "post": ["date_joined", "addresses", "last_login"],
        "patch": ["email"],
    }

    UserResource.serial_field_relations = {"Address": ["city", "state"]}

    assert UserResource._get_serializations(method="get") == (
        ["username", "company", "email"],
        {"Address": ["city", "state"]},
    )

    assert UserResource._get_serializations(method="post") == (
        ["date_joined", "addresses", "last_login"],
        {"Address": ["city", "state"]},
    )

    assert UserResource._get_serializations(method="patch") == (
        ["email"],
        {"Address": ["city", "state"]},
    )


def test__check_config_error():
    class UserResource(DBBaseResource):
        pass

    assert UserResource._check_config_error() == (
        {"message": f"Configuration error: missing model_class."},
        500,
    )

    UserResource.model_class = User

    assert UserResource._check_config_error() is None


def test_create_url():
    class UserResource(DBBaseResource):
        model_class = User
        url_name = None
        url_prefix = "/api/v2"

    # url_name is None
    assert UserResource.create_url() == "/api/v2/user"

    # another class name
    class CustomerOrder(object):
        @classmethod
        def _class(cls):
            return cls.__name__

    UserResource.model_class = CustomerOrder
    assert UserResource.create_url() == "/api/v2/customer-order"

    # url_name is valid
    UserResource.url_name = "different"
    assert UserResource.create_url() == "/api/v2/different"


def test__check_numeric_casting():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    class BookResource(DBBaseResource):
        model_class = Book

    book_data = book.to_dict(to_camel_case=False)

    # follow the filtering first as found in screen
    book_data = BookResource._remove_unnecessary_data(book_data)

    # since the source of data is from stored info in database, it is clean
    assert BookResource._check_numeric_casting(book_data) == []

    book_data["pub_year"] = "two thousand four"
    assert BookResource._check_numeric_casting(book_data) == [
        {"pub_year": "The value two thousand four is not a number"}
    ]


def test__check_max_text_lengths():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    class BookResource(DBBaseResource):
        model_class = Book

    book_data = book.to_dict(to_camel_case=False)

    # follow the filtering first as found in screen
    book_data = BookResource._remove_unnecessary_data(book_data)

    # since the source of data is from stored info in database, it is clean
    assert BookResource._check_max_text_lengths(book_data) == []

    book_data["title"] = book_data["title"] * 100

    assert BookResource._check_max_text_lengths(book_data) == [
        {"title": "The data exceeds the maximum length 100"}
    ]


def test__remove_unnecessary_data():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    class BookResource(DBBaseResource):
        model_class = Book

    book_data = book.to_dict(to_camel_case=False)

    # add another extraneous field
    book_data["test"] = "this is a"

    assert "test" not in BookResource._remove_unnecessary_data(book_data)


def test__missing_required():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    class BookResource(DBBaseResource):
        model_class = Book

    book_data = book.to_dict(to_camel_case=False)

    assert BookResource._missing_required(book_data) is None

    # delete title and author_id
    book_data.pop("title")
    book_data.pop("author_id")

    assert BookResource._missing_required(book_data) == {
        "missing_columns": ["title", "author_id"]
    }


def test_get_meta():
    """ test_get_meta

    This version does all.
    """
    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    def my_decorator():
        pass

    class BookResource(DBBaseResource):
        model_class = Book
        method_decorators = {"get": [my_decorator]}

        # since this is DBBaseResource subclassed
        # some fake methods
        def get():
            pass

        def post():
            pass

        def delete():
            pass

    assert BookResource.get_meta() == {
        "model_class": "Book",
        "url_prefix": "/",
        "url": "/book",
        "methods": {
            "get": {
                "url": "/book/<int:id>",
                "requirements": ["my_decorator"],
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
                                        "nullable": False,
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
                                        "nullable": False,
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
                                    "nullable": False,
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
    }


def test__meta_method():
    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    def my_decorator():
        pass

    class BookResource(DBBaseResource):
        model_class = Book
        method_decorators = {"get": [my_decorator]}

    assert BookResource._meta_method("get") == {
        "url": "/book/<int:id>",
        "requirements": ["my_decorator"],
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
                                "nullable": False,
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
    }

    class AuthorCollection(DBBaseResource):
        model_class = Author
        max_page_size = None  # indicator of coll

        def get(self, **kwargs):
            pass

    assert AuthorCollection.is_collection() is True

    assert AuthorCollection._meta_method("get") == {
        "url": "/author",
        "requirements": [],
        "query_string": {
            "id": {
                "type": "integer",
                "format": "int32",
                "primary_key": True,
                "nullable": False,
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
        },
        "responses": {
            "fields": {
                "id": {
                    "type": "integer",
                    "format": "int32",
                    "primary_key": True,
                    "nullable": False,
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
                "books": {
                    "readOnly": True,
                    "relationship": {
                        "type": "list",
                        "entity": "Book",
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
                        },
                    },
                },
            }
        },
    }


def test__meta_method_muliple_keys():

    db = DB(":memory:")

    # multiple keys
    class MultKeys(db.Model):
        __tablename__ = "mult_keys"
        key1 = db.Column(db.String, primary_key=True)
        key2 = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)

    db.create_all()

    class MultKeyResource(DBBaseResource):
        model_class = MultKeys

    assert MultKeyResource._meta_method("get") == {
        "url": "/mult-keys/<string:key1><int:key2>",
        "requirements": [],
        "input": [
            {
                "key1": {
                    "type": "string",
                    "primary_key": True,
                    "nullable": False,
                    "info": {},
                }
            },
            {
                "key2": {
                    "type": "integer",
                    "format": "int32",
                    "primary_key": True,
                    "nullable": False,
                    "info": {},
                }
            },
        ],
        "responses": {
            "fields": {
                "name": {"type": "string", "nullable": True, "info": {}},
                "key2": {
                    "type": "integer",
                    "format": "int32",
                    "primary_key": True,
                    "nullable": False,
                    "info": {},
                },
                "key1": {
                    "type": "string",
                    "primary_key": True,
                    "nullable": False,
                    "info": {},
                },
            }
        },
    }


def test__meta_method_decorators():
    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    def my_decorator():
        pass

    class BookResource(DBBaseResource):
        model_class = Book
        method_decorators = [my_decorator]

    class BookResource1(DBBaseResource):
        model_class = Book
        method_decorators = {"get": [my_decorator]}

    assert BookResource._meta_method_decorators("get") == ["my_decorator"]

    assert BookResource1._meta_method_decorators("get") == ["my_decorator"]

    assert BookResource._meta_method_decorators("post") == ["my_decorator"]

    assert BookResource1._meta_method_decorators("post") == []


def test__meta_method_response():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    def my_decorator():
        pass

    class BookResource(DBBaseResource):
        model_class = Book
        method_decorators = [my_decorator]

    assert BookResource._meta_method_response("get") == {
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
                            "nullable": False,
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
    }
