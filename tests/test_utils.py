# tests/test_dbbase_resource.py
import pytest
from flask_restful_dbbase.utils import MetaDoc


def test_MetaDoc():

    meta_doc = MetaDoc()

    assert meta_doc.process_get_input is None
    assert meta_doc.process_post_input is None
    assert meta_doc.process_put_input is None
    assert meta_doc.process_patch_input is None
    assert meta_doc.process_delete_input is None

    assert meta_doc._before_commit == {}
    assert meta_doc._after_commit == {}

    meta_doc = MetaDoc(
        process_get_input="This doc is for process_get_input.",
        process_post_input="This doc is for process_get_post.",
        process_put_input="This doc is for process_put_input.",
        process_patch_input="This doc is for process_patch_input.",
        process_delete_input="This doc is for process_delete_input.",
        before_commit={"post": "this is post", "put": "this is put"},
        after_commit={"post": "this is post", "put": "this is put"},
        excludes=["get", "post"],
    )

    assert meta_doc.process_get_input == "This doc is for process_get_input."
    assert meta_doc.process_post_input == "This doc is for process_get_post."
    assert meta_doc.process_put_input == "This doc is for process_put_input."
    assert (
        meta_doc.process_patch_input == "This doc is for process_patch_input."
    )
    assert (
        meta_doc.process_delete_input
        == "This doc is for process_delete_input."
    )
    assert meta_doc._before_commit == {
        "post": "this is post",
        "put": "this is put",
    }
    assert meta_doc._after_commit == {
        "post": "this is post",
        "put": "this is put",
    }

    assert meta_doc.excludes == set(["get", "post"])


def test_Meta_doc_before_commit():

    meta_doc = MetaDoc()

    with pytest.raises(ValueError) as err:
        meta_doc.before_commit("get", "this is a test")

    assert str(err.value) == "This method is not valid"
    with pytest.raises(ValueError) as err:
        meta_doc.after_commit("get", "this is a test")

    assert str(err.value) == "This method is not valid"

    meta_doc.before_commit("post", "this is a test")
    assert meta_doc._before_commit["post"] == "this is a test"

    meta_doc.after_commit("post", "this is a test")
    assert meta_doc._after_commit["post"] == "this is a test"
