# tests/test_dbbase_resource.py
import pytest
from dbbase import DB

from flask_restful_dbbase.doc_utils import MetaDoc, MethodDoc
from flask_restful_dbbase.resources import (
    ModelResource,
    CollectionModelResource,
    MetaResource,
)


def test_create_doc():

    db = DB(":memory:")

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

    class Job(db.Model):
        __tablename__ = "job"
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        job_name = db.Column(db.String(100), nullable=False)

    class MultipleKey(db.Model):
        __tablename__ = "mult_key"
        id1 = db.Column(db.Integer, nullable=True, primary_key=True)
        id2 = db.Column(db.Integer, nullable=True, primary_key=True)

    db.create_all()

    class AuthorResource(ModelResource):
        model_class = Author
        serial_fields = {"post": {Job: ["id", "job_name"]}}

    class AuthorCollectionResource(CollectionModelResource):
        model_class = Author

    class AuthorMetaResource(MetaResource):
        resource_class = AuthorResource

    class AuthorCollectionMetaResource(MetaResource):
        resource_class = AuthorCollectionResource

    with pytest.raises(ValueError) as err:
        MetaDoc(resource_class=AuthorResource, methods="potato")

    assert str(err.value) == "methods must be a dictionary"

    meta_doc = MetaDoc(resource_class=AuthorResource)

    assert meta_doc.resource_class == AuthorResource
    assert meta_doc.model_class == Author._class()
    assert meta_doc.url_prefix == AuthorResource.url_prefix
    assert meta_doc.base_url == AuthorResource.create_url()
    assert meta_doc.methods == {}
    assert meta_doc.table is None

    post_method_doc = MethodDoc(method="post")

    assert post_method_doc.input is None
    assert post_method_doc.input_modifier is None
    assert post_method_doc.before_commit is None
    assert post_method_doc.after_commit is None
    assert post_method_doc.responses == []

    post_method_doc.input_modifier = "this describes the input_modifier"
    post_method_doc.before_commit = "this describes the before_commit"
    post_method_doc.after_commit = "this describes the after_commit"

    assert post_method_doc.to_dict(meta_doc) == {
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
        "input_modifier": "this describes the input_modifier",
        "before_commit": "this describes the before_commit",
        "after_commit": "this describes the after_commit",
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
                    "jobName": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": False,
                        "info": {},
                    },
                }
            }
        ],
    }
    # shows a job returned
    meta_doc.methods["post"] = post_method_doc

    assert meta_doc.to_dict() == {
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
                "responses": [
                    {
                        "fields": {
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
                            "fullName": {"readOnly": True},
                            "firstName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
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
                "input_modifier": "this describes the input_modifier",
                "before_commit": "this describes the before_commit",
                "after_commit": "this describes the after_commit",
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
                            "jobName": {
                                "type": "string",
                                "maxLength": 100,
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
                "responses": [
                    {
                        "fields": {
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
                            "fullName": {"readOnly": True},
                            "firstName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
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
                "responses": [
                    {
                        "fields": {
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
                            "fullName": {"readOnly": True},
                            "firstName": {
                                "type": "string",
                                "maxLength": 50,
                                "nullable": False,
                                "info": {},
                            },
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": True,
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
    get_method_doc = MethodDoc(method="get")
    put_method_doc = MethodDoc(method="put")
    patch_method_doc = MethodDoc(method="patch")
    delete_method_doc = MethodDoc(method="delete")

    assert get_method_doc.to_dict(meta_doc=meta_doc) == {
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
        "responses": [
            {
                "fields": {
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
                    "fullName": {"readOnly": True},
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": True,
                        "nullable": False,
                        "info": {},
                    },
                }
            }
        ],
    }

    assert put_method_doc.to_dict(meta_doc=meta_doc) == {
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
        "responses": [
            {
                "fields": {
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
                    "fullName": {"readOnly": True},
                    "lastName": {
                        "type": "string",
                        "maxLength": 50,
                        "nullable": False,
                        "info": {},
                    },
                }
            }
        ],
    }

    assert patch_method_doc.to_dict(meta_doc=meta_doc) == {
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
        "responses": [
            {
                "fields": {
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
                    "fullName": {"readOnly": True},
                    "lastName": {
                        "type": "string",
                        "maxLength": 50,
                        "nullable": False,
                        "info": {},
                    },
                }
            }
        ],
    }

    assert delete_method_doc.to_dict(meta_doc=meta_doc) == {
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
        "responses": [{}],
    }

    # test collections
    collection_meta_doc = MetaDoc(resource_class=AuthorCollectionResource)

    get_method_doc = MethodDoc(method="get")

    assert get_method_doc.to_dict(meta_doc=collection_meta_doc) == {
        "url": "/authors",
        "requirements": [],
        "queryString": {
            "id": {
                "type": "integer",
                "format": "int32",
                "primary_key": True,
                "nullable": False,
                "info": {},
            }
        },
        "jobParams": {
            "orderBy": {"type": "string", "list": True},
            "maxPageSize": {"type": "integer"},
            "offset": {"type": "integer"},
            "debug": {"type": "boolean"},
        },
        "responses": [
            {
                "fields": {
                    "firstName": {
                        "type": "string",
                        "maxLength": 50,
                        "nullable": False,
                        "info": {},
                    },
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": True,
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
                    "fullName": {"readOnly": True},
                }
            }
        ],
    }

    # multiple keys
    class MultKeyResource(ModelResource):
        model_class = MultipleKey

    assert MethodDoc._get_input_keys(MultKeyResource) == [
        {
            "id1": {
                "type": "integer",
                "format": "int32",
                "primary_key": True,
                "nullable": True,
                "info": {},
            }
        },
        {
            "id2": {
                "type": "integer",
                "format": "int32",
                "primary_key": True,
                "nullable": True,
                "info": {},
            }
        },
    ]

    # custom response
    method_doc = MethodDoc(
        "post",
        use_default_response=False,
        responses=[{"message": "a unique response"}],
    )

    MetaDoc(
        resource_class=MultKeyResource,
        methods={method_doc.method: method_doc},
    )

    assert method_doc.to_dict(meta_doc) == {
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
        "responses": [{"message": "a unique response"}],
    }
