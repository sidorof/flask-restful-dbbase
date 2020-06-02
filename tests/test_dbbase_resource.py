# tests/test_dbbase_resource.py
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

        id = db.Column(db.Integer, primary_key=True)
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

    resource = DBBaseResource
    resource.model_class = User

    assert resource.get_key(formatted=False) == "username"
    assert resource.get_key(formatted=True) == "<string:username>"

    resource = DBBaseResource
    resource.model_class = Address

    assert resource.get_key(formatted=False) == "id"
    assert resource.get_key(formatted=True) == "<int:id>"


def test_get_obj_params():

    resource = DBBaseResource
    resource.model_class = User

    obj_params = resource.get_obj_params()

    expected_result = {
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
            "relationship": {"type": "list", "entity": "Address"},
        },
    }

    assert obj_params == expected_result


def test_get_obj_params_with_colprops():
    """
    Test with column property filtering
    """
    resource = DBBaseResource
    resource.model_class = User

    obj_params = resource.get_obj_params(column_props=["type", "nullable"])

    expected_result = {
        "username": {"type": "string", "nullable": False},
        "password": {"type": "string", "nullable": False},
        "email": {"type": "string", "nullable": False},
        "first_name": {"type": "string", "nullable": True},
        "last_name": {"type": "string", "nullable": True},
        "company": {"type": "string", "nullable": True},
        "is_superuser": {"type": "boolean", "nullable": False},
        "is_staff": {"type": "boolean", "nullable": False},
        "is_active": {"type": "boolean", "nullable": False},
        "is_account_current": {"type": "boolean", "nullable": False},
        "date_joined": {"type": "date", "nullable": False},
        "last_login": {"type": "date-time", "nullable": True},
        "addresses": {},
    }

    assert obj_params == expected_result


def test_pre_save():
    """
    Prototype functions
    """
    item = "this is a test"
    self = None
    assert DBBaseResource.pre_save(self, item) == item


def test_post_save():
    """
    Prototype functions
    """
    item = "this is a test"
    self = None
    assert DBBaseResource.post_save(self, item) == item


def test_format_key():

    key = "test"
    key_type = "integer"

    assert DBBaseResource.format_key(key, key_type) == "<int:test>"

    key_type = "string"

    assert DBBaseResource.format_key(key, key_type) == "<string:test>"


def test_get_urls():

    resource = DBBaseResource
    resource.model_class = User

    urls = resource.get_urls()

    assert urls == ["/user", "/user/<string:username>"]

    resource.url_prefix = "/api/v1"
    resource.url_name = "users"

    urls = resource.get_urls()

    assert urls == ["/api/v1/users", "/api/v1/users/<string:username>"]


def test_get_meta():

    print("test_get_meta is not done")


def test__check_key():

    resource = DBBaseResource
    resource.model_class = User

    kwargs = {"username": "test"}

    # finds the key
    assert resource._check_key(kwargs) == ("username", "test")

    kwargs = {"something": "else"}

    # does not find the key
    assert resource._check_key(kwargs) == ({"message": "invalid key"}, None)


def test__get_serial_fields():

    resource = DBBaseResource
    resource.model_class = User

    # nothing special for methods
    assert (
        resource._get_serial_fields(method="something")
        == resource.model_class.get_serial_fields()
    )

    resource.serial_fields = {
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

    assert resource._get_serial_fields(method="get") == [
        "username",
        "company",
        "email",
    ]

    assert resource._get_serial_fields(method="post") == [
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

    assert resource._get_serial_fields(method="patch") == ["email"]

    # unspecified for particular method, but still a dict
    assert set(resource._get_serial_fields(method="put")) == set(
        resource.model_class.get_serial_fields()
    )


def test__get_serial_field_relations():

    resource = DBBaseResource
    resource.model_class = User

    User.SERIAL_FIELD_RELATIONS = {"Address": ["city", "state"]}

    assert resource._get_serial_field_relations(method="get") == {
        "Address": ["city", "state"]
    }

    resource.serial_field_relations = {
        "get": {"Address": ["city"]},
        "post": {"Address": ["city", "state", "company"]},
    }

    assert resource._get_serial_field_relations("get") == {"Address": ["city"]}

    assert resource._get_serial_field_relations("post") == {
        "Address": ["city", "state", "company"]
    }

    assert resource._get_serial_field_relations("other") == {
        "Address": ["city", "state"]
    }


def test__get_serializations():

    resource = DBBaseResource
    resource.model_class = User

    resource.serial_fields = {
        "get": ["username", "company", "email"],
        "post": ["date_joined", "addresses", "last_login"],
        "patch": ["email"],
    }

    resource.serial_field_relations = {"Address": ["city", "state"]}

    assert resource._get_serializations(method="get") == (
        ["username", "company", "email"],
        {"Address": ["city", "state"]},
    )

    assert resource._get_serializations(method="post") == (
        ["date_joined", "addresses", "last_login"],
        {"Address": ["city", "state"]},
    )

    assert resource._get_serializations(method="patch") == (
        ["email"],
        {"Address": ["city", "state"]},
    )


def test__check_config_error():

    resource = DBBaseResource
    resource.model_class = None

    assert resource._check_config_error() == (
        {"message": f"Configuration error: missing model_class."},
        500,
    )

    resource.model_class = User

    assert resource._check_config_error() is None


def test_create_url():

    resource = DBBaseResource
    resource.model_class = User
    resource.url_name = None
    resource.url_prefix = "/api/v2"

    # url_name is None
    assert resource.create_url() == "/api/v2/user"

    # another class name
    class CustomerOrder(object):
        @classmethod
        def _class(cls):
            return cls.__name__

    resource.model_class = CustomerOrder
    assert resource.create_url() == "/api/v2/customer-order"

    # url_name is valid
    resource.url_name = "different"
    assert resource.create_url() == "/api/v2/different"


def test_screen_data():
    """
    test_screen_data


    This function and the next few are concerned with the
    evaluation of incoming data in light of the requirements
    of the model for complete information.

    This will use the book and author example with a few
    pretend records.
    """
    # test_screen_data(
    #    data,
    #    obj_params,
    #    skip_missing_data=False)
    pass


def test__check_numeric_casting():

    # db1 = DB(config="sqlite:///test1231.db")
    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    resource = DBBaseResource
    resource.model_class = Book

    obj_params = resource.get_obj_params()
    book_data = book.to_dict(to_camel_case=False)

    # follow the filtering first as found in screen
    book_data = resource._remove_unnecessary_data(book_data, obj_params)

    # since the source of data is from stored info in database, it is clean
    assert resource._check_numeric_casting(book_data, obj_params) == []

    book_data["pub_year"] = "two thousand four"
    assert resource._check_numeric_casting(book_data, obj_params) == [
        {"pub_year": "The value two thousand four is not a number"}
    ]


def test__check_max_text_lengths():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    resource = DBBaseResource
    resource.model_class = Book

    obj_params = resource.get_obj_params()
    book_data = book.to_dict(to_camel_case=False)

    # follow the filtering first as found in screen
    book_data = resource._remove_unnecessary_data(book_data, obj_params)

    # since the source of data is from stored info in database, it is clean
    assert resource._check_max_text_lengths(book_data, obj_params) == []

    book_data["title"] = book_data["title"] * 100

    assert resource._check_max_text_lengths(book_data, obj_params) == [
        {"title": "The data exceeds the maximum length 100"}
    ]


def test__remove_unnecessary_data():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    resource = DBBaseResource
    resource.model_class = Book

    obj_params = resource.get_obj_params()
    obj_params = resource._exclude_read_only(obj_params)
    book_data = book.to_dict(to_camel_case=False)

    # add another extraneous field
    book_data["test"] = "this is a"

    assert "test" not in resource._remove_unnecessary_data(
        book_data, obj_params
    )


def test__missing_required():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    resource = DBBaseResource
    resource.model_class = Book

    obj_params = resource.get_obj_params()
    obj_params = resource._exclude_read_only(obj_params)
    book_data = book.to_dict(to_camel_case=False)

    assert resource._missing_required(book_data, obj_params) is None

    # delete title and author_id
    book_data.pop("title")
    book_data.pop("author_id")

    assert resource._missing_required(book_data, obj_params) == {
        "missing_columns": ["title", "author_id"]
    }


def test__exclude_read_only():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    resource = DBBaseResource
    resource.model_class = Book

    obj_params = resource.get_obj_params()

    obj_params_copy = dict([[key, value] for key, value in obj_params.items()])
    obj_params_copy.pop("author")

    assert resource._exclude_read_only(obj_params) == obj_params_copy


def test__get_required():

    db1 = DB(config=":memory:")
    Author, Book, author, book = create_models(db1)

    resource = DBBaseResource
    resource.model_class = Book

    obj_params = resource.get_obj_params()

    # required fields are title, author_id, pub_year
    # NOTE: check this. an id can be assigned a default, but not really
    # required t
    assert set(resource._get_required(obj_params)) == set(
        ["id", "title", "author_id", "pub_year"]
    )
