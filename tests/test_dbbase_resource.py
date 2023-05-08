# tests/test_dbbase_resource.py
import pytest
from datetime import date, datetime
from dbbase import DB
from flask_restful_dbbase.resources import DBBaseResource
from flask_restful_dbbase.doc_utils import MetaDoc, MethodDoc
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


def test_get_key_names():
    class UserResource(DBBaseResource):
        model_class = User

    assert UserResource.get_key_names(formatted=False) == ["username"]
    assert UserResource.get_key_names(formatted=True) == ["<string:username>"]

    class AddressResource(DBBaseResource):
        model_class = Address

    assert AddressResource.get_key_names(formatted=False) == ["id"]
    assert AddressResource.get_key_names(formatted=True) == ["<int:id>"]


def test_get_obj_params():
    class UserResource(DBBaseResource):
        model_class = User

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
            "readOnly": False,
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

        def get(self):
            """To trigger keys to show"""
            pass

    urls = UserResource.get_urls()

    assert urls == ["/users", "/users/<string:username>"]

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
    db = DB(config="sqlite:///:memory:")

    class MultKey(db.Model):
        __tablename__ = "mult_keys"
        key1 = db.Column(db.String, primary_key=True)
        key2 = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String)

    db.create_all()

    class MultKeyResource(DBBaseResource):
        model_class = MultKey

        def get(self):
            """To trigger keys to show"""
            pass

    assert MultKeyResource.get_urls() == [
        "/mult-keys",
        "/mult-keys/<string:key1><int:key2>",
    ]


def test__check_key():
    class UserResource(DBBaseResource):
        model_class = User

    kwargs = {"username": "test"}

    # finds the key
    assert UserResource()._check_key(kwargs) == {"username": "test"}

    kwargs = {"something": "else"}

    # does not find the key
    pytest.raises(ValueError, UserResource()._check_key, kwargs)


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


def test__get_serial_fields_foreign_class():
    class UserResource(DBBaseResource):
        serial_fields = {"post": {Address: ["city", "state"]}}

    assert UserResource._get_serial_fields(method="post", with_class=True) == {
        Address: ["city", "state"]
    }

    assert UserResource._get_serial_fields(
        method="post", with_class=False
    ) == ["city", "state"]


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
        {"message": "Configuration error: missing model_class."},
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
    assert UserResource.create_url() == "/api/v2/users"

    # another class name
    class CustomerOrder(object):
        @classmethod
        def _class(cls):
            return cls.__name__

    UserResource.model_class = CustomerOrder
    assert UserResource.create_url() == "/api/v2/customer-orders"

    # url_name is valid
    UserResource.url_name = "different"
    assert UserResource.create_url() == "/api/v2/different"


def test__check_numeric_casting():
    # valid
    assert (
        DBBaseResource._check_numeric_casting(
            col_key="key", value=100, col_params={"type": "integer"}
        )
        == []
    )

    # valid
    assert (
        DBBaseResource._check_numeric_casting(
            col_key="key", value=100, col_params={"type": "float"}
        )
        == []
    )

    # valid
    assert (
        DBBaseResource._check_numeric_casting(
            col_key="key", value=100.23456, col_params={"type": "float"}
        )
        == []
    )

    # invalid
    assert DBBaseResource._check_numeric_casting(
        col_key="key", value="one hundred", col_params={"type": "float"}
    ) == [{"key": "The value one hundred is not a number"}]

    # pass by
    assert (
        DBBaseResource._check_numeric_casting(
            col_key="key", value="one hundred", col_params={"type": "string"}
        )
        == []
    )

    # None
    assert (
        DBBaseResource._check_numeric_casting(
            col_key="key", value=None, col_params={"type": "integer"}
        )
        == []
    )


def test__check_max_text_lengths():
    # valid
    assert (
        DBBaseResource._check_max_text_lengths(
            col_key="key", value="this is a test", col_params={"maxLength": 20}
        )
        == []
    )

    # invalid
    assert DBBaseResource._check_max_text_lengths(
        col_key="key", value="this is a test", col_params={"maxLength": 5}
    ) == [{"key": "The data exceeds the maximum length 5"}]

    # pass by
    assert (
        DBBaseResource._check_max_text_lengths(
            col_key="key", value="this is a test", col_params={}
        )
        == []
    )

    # None
    assert (
        DBBaseResource._check_max_text_lengths(
            col_key="key", value=None, col_params={"maxLength": 20}
        )
        == []
    )


def test__check_date_casting():
    # DBBaseResource.use_date_conversions = True

    # valid - date
    assert DBBaseResource._check_date_casting(
        col_key="key", value="2014-11-01", col_params={"type": "date"}
    ) == (True, date(2014, 11, 1))

    # invalid format - date
    assert DBBaseResource._check_date_casting(
        col_key="key", value="blah, blah", col_params={"type": "date"}
    ) == (
        False,
        [
            {
                "key": "Date error: 'blah, blah': Unknown string format: blah, blah"
            }
        ],
    )

    # valid - datetime
    assert DBBaseResource._check_date_casting(
        col_key="key", value="2014-11-01", col_params={"type": "date-time"}
    ) == (True, datetime(2014, 11, 1))

    # invalid format - date
    assert DBBaseResource._check_date_casting(
        col_key="key", value="blah, blah", col_params={"type": "date-time"}
    ) == (
        False,
        [
            {
                "key": "Date error: 'blah, blah': Unknown string format: blah, blah"
            }
        ],
    )

    # None
    assert DBBaseResource._check_date_casting(
        col_key="key", value=None, col_params={"type": "date-time"}
    ) == (True, None)


def test_screen_data():
    """
    Coverage from other tests except for
    date related.
    """
    db = DB(config="sqlite:///:memory:")

    class AModel(db.Model):
        __tablename__ = "amodel"
        id = db.Column(db.Integer, primary_key=True)
        today = db.Column(db.Date)

    data = {"today": "2020-3-4"}
    obj_params = {"today": {"type": "date"}}

    class TestResource(DBBaseResource):
        model_class = AModel
        use_date_conversions = True

    assert TestResource().screen_data(data, obj_params) == (
        True,
        {"today": date(2020, 3, 4)},
    )


def test_get_meta():
    """test_get_meta

    This version does all.
    """
    db1 = DB(config="sqlite:///:memory:")
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
        "modelClass": "Book",
        "urlPrefix": "/",
        "baseUrl": "/books",
        "methods": {
            "get": {
                "url": "/books/<int:id>",
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
                "responses": [
                    {
                        "fields": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            },
                            "pubYear": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
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
                            "authorId": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "foreign_key": "author.id",
                                "info": {},
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
                        }
                    }
                ],
            },
            "post": {
                "url": "/books",
                "requirements": None,
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
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": True,
                                "info": {},
                            },
                            "pubYear": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
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
                            "authorId": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": False,
                                "foreign_key": "author.id",
                                "info": {},
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
                        }
                    }
                ],
            },
            "delete": {
                "url": "/books/<int:id>",
                "requirements": None,
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


def test__all_keys_found():
    data = {"key1": 1, "key2": 2, "extra": True}

    # key_names is a string
    key_names = "key1"
    assert DBBaseResource._all_keys_found(key_names, data) == (
        True,
        {key_names: data[key_names]},
    )

    key_names = "different"
    assert DBBaseResource._all_keys_found(key_names, data) == (False, {})

    # key_names is a list of key_names
    key_names = ["key1", "key2"]

    assert DBBaseResource._all_keys_found(key_names, data) == (
        True,
        {"key1": 1, "key2": 2},
    )

    # partial fit
    data = {"key1": 1, "extra": True}
    assert DBBaseResource._all_keys_found(key_names, data) == (False, {})


def test__item_adjust():
    def bad_func(self, item, status_code):
        return "invalid response"

    pytest.raises(
        ValueError,
        DBBaseResource._item_adjust,
        DBBaseResource,
        bad_func,
        "nothing",
        200,
    )


def test_input_processing():
    db10 = DB(config="sqlite:///:memory:")
    Author, Book, author, book = create_models(db10)

    class TestResource(DBBaseResource):
        model_class = Author

        def get():
            pass

        def post():
            pass

        def put():
            pass

        def patch():
            pass

        def delete():
            pass

    meta_doc = MetaDoc(
        resource_class=TestResource,
        methods=[
            MethodDoc(
                method="get",
                input_modifier="This doc is for process_get_input.",
                before_commit="This doc is for before_commit in get",
                after_commit="This doc is for after_commit in get",
            ),
            MethodDoc(
                method="post",
                input_modifier="This doc is for process_post_input.",
                before_commit="This doc is for before_commit in post",
                after_commit="This doc is for after_commit in post",
            ),
            MethodDoc(
                method="put",
                input_modifier="This doc is for process_put_input.",
                before_commit="This doc is for before_commit in put",
                after_commit="This doc is for after_commit in put",
            ),
            MethodDoc(
                method="patch",
                input_modifier="This doc is for process_patch_input.",
                before_commit="This doc is for before_commit in patch",
                after_commit="This doc is for after_commit in patch",
            ),
            MethodDoc(
                method="delete",
                input_modifier="This doc is for process_delete_input.",
                before_commit="This doc is for before_commit in delete",
                after_commit="This doc is for after_commit in delete",
            ),
        ],
    )

    assert TestResource.meta_doc is None

    TestResource.meta_doc = meta_doc
    assert isinstance(TestResource.meta_doc, MetaDoc)

    assert TestResource.get_meta() == {
        "modelClass": "Author",
        "urlPrefix": "/",
        "baseUrl": "/authors",
        "methods": {
            "get": {
                "url": "/authors/<int:id>",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": True,
                        "nullable": False,
                        "info": {},
                    }
                },
                "input_modifier": "This doc is for process_get_input.",
                "before_commit": "This doc is for before_commit in get",
                "after_commit": "This doc is for after_commit in get",
                "responses": [
                    {
                        "fields": {
                            "lastName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                            "fullName": {"readOnly": True},
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": False,
                                "info": {},
                            },
                            "books": {
                                "readOnly": False,
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
                                },
                            },
                            "firstName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                        }
                    }
                ],
            },
            "post": {
                "url": "/authors",
                "requirements": [],
                "input": {
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
                    "books": {
                        "readOnly": False,
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
                        },
                    },
                },
                "input_modifier": "This doc is for process_post_input.",
                "before_commit": "This doc is for before_commit in post",
                "after_commit": "This doc is for after_commit in post",
                "responses": [
                    {
                        "fields": {
                            "lastName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                            "fullName": {"readOnly": True},
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": False,
                                "info": {},
                            },
                            "books": {
                                "readOnly": False,
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
                                },
                            },
                            "firstName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                        }
                    }
                ],
            },
            "put": {
                "url": "/authors/<int:id>",
                "requirements": [],
                "input": {
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
                    "books": {
                        "readOnly": False,
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
                        },
                    },
                },
                "input_modifier": "This doc is for process_put_input.",
                "before_commit": "This doc is for before_commit in put",
                "after_commit": "This doc is for after_commit in put",
                "responses": [
                    {
                        "fields": {
                            "lastName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                            "fullName": {"readOnly": True},
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": False,
                                "info": {},
                            },
                            "books": {
                                "readOnly": False,
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
                                },
                            },
                            "firstName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                        }
                    }
                ],
            },
            "patch": {
                "url": "/authors/<int:id>",
                "requirements": [],
                "input": {
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
                    "books": {
                        "readOnly": False,
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
                        },
                    },
                },
                "input_modifier": "This doc is for process_patch_input.",
                "before_commit": "This doc is for before_commit in patch",
                "after_commit": "This doc is for after_commit in patch",
                "responses": [
                    {
                        "fields": {
                            "lastName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                            "fullName": {"readOnly": True},
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
                                "nullable": False,
                                "info": {},
                            },
                            "books": {
                                "readOnly": False,
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
                                },
                            },
                            "firstName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                        }
                    }
                ],
            },
            "delete": {
                "url": "/authors/<int:id>",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": True,
                        "nullable": False,
                        "info": {},
                    }
                },
                "input_modifier": "This doc is for process_delete_input.",
                "before_commit": "This doc is for before_commit in delete",
                "after_commit": "This doc is for after_commit in delete",
                "responses": [{}],
            },
        },
        "table": {
            "Author": {
                "type": "object",
                "properties": {
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
                        "readOnly": False,
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
                },
                "xml": "Author",
            }
        },
    }
