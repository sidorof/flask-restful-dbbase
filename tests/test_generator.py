# tests/test_generator.py
import pytest
from dbbase import DB
from flask_restful_dbbase.resources import (
    ModelResource,
    CollectionModelResource,
)
from flask_restful_dbbase.generator import create_resource


def test_create_resources():

    db = DB("sqlite:///:memory:")

    class Book(db.Model):
        __tablename__ = "book"

        id = db.Column(db.Integer, primary_key=True)
        description = db.Column(db.String(50), nullable=False)

    db.create_all()

    # no model class
    with pytest.raises(ValueError) as err:
        new_resource = create_resource(
            Book._class(),
            resource_class=ModelResource,
        )
    assert str(err.value) == "A model class must be defined"

    new_resource = create_resource(
        f"{Book._class()}{ModelResource.__name__}",
        resource_class=ModelResource,
        model_class=Book,
    )

    assert new_resource.__name__ == "BookModelResource"
    assert new_resource.model_class == Book
    assert new_resource.url_prefix == "/"
    assert new_resource.get_urls() == ["/books", "/books/<int:id>"]

    for attr in ["get", "post", "put", "patch", "delete"]:
        assert hasattr(new_resource, attr)

    # applying class variables
    class_vars = {
        "method_decorators": "test1",
        "process_get_input": "test2",
        "process_post_input": "test3",
        "process_put_input": "test4",
        "process_patch_input": "test5",
        "process_delete_input": "test6",
        "before_commit": "test7",
        "after_commit": "test8",
    }

    new_resource = create_resource(
        Book._class(),
        resource_class=ModelResource,
        model_class=Book,
        methods=["get"],
        url_prefix="/api/v1",
        url_name="different",
        class_vars=class_vars,
    )

    assert new_resource.methods == {"GET"}
    assert new_resource.url_prefix == "/api/v1"
    assert new_resource.url_name == "different"
    assert new_resource.get_urls() == [
        "/api/v1/different",
        "/api/v1/different/<int:id>",
    ]

    for cvar, value in class_vars.items():
        assert getattr(new_resource, cvar) == value

    PostOnly = create_resource(
        "PostOnly",
        resource_class=ModelResource,
        model_class=Book,
        methods=["post"],
    )

    assert hasattr(PostOnly, "get") is False
    assert hasattr(PostOnly, "put") is False
    assert hasattr(PostOnly, "patch") is False
    assert hasattr(PostOnly, "delete") is False
    assert PostOnly.methods == set(["POST"])

    # test collection
    new_collection_resource = create_resource(
        f"{Book._class()}CollectionModelResource",
        resource_class=CollectionModelResource,
        model_class=Book,
    )

    assert hasattr(new_collection_resource, "max_page_size")

    assert new_collection_resource.model_class == Book
    assert new_collection_resource.url_prefix == "/"
    assert new_collection_resource.get_urls() == ["/books"]
