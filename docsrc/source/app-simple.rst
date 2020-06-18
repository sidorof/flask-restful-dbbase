------------
A First Look
------------
We will create a small app that shows some of the capabilities.

First, we import and configure the database. Within the Flask environment, DBBase provides a thin wrapper around Flask-SQLAlchemy but with a different Model class.

The data-aware resources are then imported. Once that is done a couple database models are created that we will use for our example.

Flask-RESTful Resource subclasses implement this functionality.

* :class:`~flask_restful_dbbase.resources.ModelResource` -- This class implements the standard methods associated with interacting with a single record, namely GET, POST, PUT, PATCH, and DELETE.
* :class:`~flask_restful_dbbase.resources.CollectionModelResource` -- This class implements a GET for collections. The other methods, being less common for collections, have been left off to avoid activating an unwanted (surprise) capability.
* :class:`~flask_restful_dbbase.resources.MetaResource` -- This class implements a GET that documents the capabilities of a resource class.


Initialize the App and Models
-----------------------------

.. code-block:: python

    from flask import Flask
    from flask_restful import Api
    from flask_restful_dbbase import DBBase

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    api = Api(app)
    db = DBBase(app)

    from flask_restful_dbbase.resources import (
        CollectionModelResource,
        ModelResource,
        MetaResource
    )

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

..

Next some sample records are created so that we have something to look at.

.. code-block:: python

    author = Author(
        first_name="Geoffrey", last_name="Cooper").save()

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

..

Create Resources
----------------

Now we can create some resources that will use these models.

.. code-block:: python

    class BookCollection(CollectionModelResource):
        model_class = Book
        url_name = "books"

    class BookResource(ModelResource):
        model_class = Book
        url_name = "books"

    class AuthorCollection(CollectionModelResource):
        model_class = Author
        url_name = "authors"

    class AuthorResource(ModelResource):
        model_class = Author
        url_name = "authors"

..

So what will this do? Once added to the API, the methods GET, POST, PUT, PATCH, and DELETE will be available at the default URLs of:

.. code-block::

    /books              <-- the collection resource URL
    /books              <-- the URL for post
    /books/<int:id>     <-- the URL for get/put/patch/delete

    /authors            <-- the collection resource URL
    /authors            <-- the URL for post
    /authors/<int:id>   <-- the URL for get/put/patch/delete

..

Another resource type, the :class:`~flask_restful_dbbase.resources.MetaResource`, can provide detailed information about your API and the requirements and capabilities by URL.

Such meta resources are created by informing the meta resource of the resource class.

.. code-block:: python

    class BookMetaCollection(MetaResource):
        resource_class = BookCollection

    class BookMeta(MetaResource):
        resource_class = BookResource

    class AuthorMetaCollection(MetaResource):
        resource_class = AuthorCollection

    class AuthorMeta(MetaResource):
        resource_class = AuthorResource

..

Once added to the API,  The following URLs will become available.

.. code-block::

    /meta/authors/single
    /meta/authors/collection
    /meta/books/single
    /meta/books/collection

..

Finally, the resources are added to the api. You can see below that the URLs are generated by the resources themselves. These functions are for convenience, the URLs ca also be added in the usual way with Flask-RESTful as well.

.. code-block:: python

    api.add_resource(AuthorCollection, *AuthorCollection.get_URLs())
    api.add_resource(AuthorResource, *AuthorResource.get_URLs())
    api.add_resource(AuthorMetaCollection, *AuthorMetaCollection.get_URLs())
    api.add_resource(AuthorMeta, *AuthorMeta.get_URLs())

    api.add_resource(BookCollection, *BookCollection.get_URLs())
    api.add_resource(BookResource, *BookResource.get_URLs())
    api.add_resource(BookMetaCollection, *BookMetaCollection.get_URLs())
    api.add_resource(BookMeta, *BookMeta.get_URLs())


    if __name__ == "__main__":
        app.run(debug=True)

..

Use the API
---------------------

As a first step, let us get a book.

.. code-block::

    curl http://localhost:5000/book/1

..

.. code-block:: json

    {
        "isbn": "0-87893-214-3",
        "title": "The Cell: A Molecular Approach, 3rd edition",
        "authorId": 1,
        "id": 1,
        "author": {
            "fullName": "Geoffrey Cooper",
            "id": 1,
            "firstName": "Geoffrey",
            "lastName": "Cooper"
        },
        "pubYear": 2004
    }

..

Note that the column names have been converted to camel case. Also, because a relationship has been specified in the table, the author has been included by default. As to what shows or does not, that is under your control through configuration.

Now we will post some data. But first, let's do it wrong.

.. code-block:: bash

    curl http://localhost:5000/books \
        -d author_id=1 \
        -d title="this is a test woah, this is really a long title, woah, this is really a long title, woah, this is really a long title, woah, this is really a long title, woah, this is really a long title "

..

Here we get back an error message. Data validation compares the data received versus what can posted to the database. An attempt is made to provide meaningful errors so that an appropriate action can be taken. In this case the publication year is missing and the title is too long.

.. code-block:: json

    {
        "message": [
            {
                "missing_columns": ["pub_year"]
            },
            {
                "title": "The data exceeds the maximum length 100"
            }
        ]
    }

..

Now we post a book that does not have errors:

.. code-block:: bash

    curl http://localhost:5000/books \
        -d author_id=3 \
        -d title="The Algorithm Design Manual" \
        -d pubYear=1997 \
        -d isbn="0-387-94860-0"

..

.. code-block:: json

    {
        "id": 6,
        "authorId": 3,
        "author": {
            "id": 3,
            "fullName": "Steven Skiena",
            "lastName": "Skiena",
            "firstName": "Steven"
        },
        "isbn": "0-387-94860-0",
        "pubYear": 1997,
        "title": "The Algorithm Design Manual"
    }

..


Meta Information
----------------

Finally, we can document our API using meta information.

.. code-block:: bash

    curl -g http://localhost:5000/meta/books/single

..

The following output details the entire book resource. Incidently, we could have also specified `curl -g http://localhost:5000/meta/books/single?get` to see only the GET method requirements.

.. code-block:: json


    {
        "model_class": "Book",
        "url_prefix": "/",
        "url": "/books",
        "methods": {
            "get": {
                "url": "/books/<int:id>",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "author_id": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "author.id",
                            "info": {}
                        },
                        "author": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Author"
                            }
                        },
                        "isbn": {
                            "type": "string",
                            "maxLength": 20,
                            "nullable": true,
                            "info": {}
                        },
                        "pub_year": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "info": {}
                        },
                        "title": {
                            "type": "string",
                            "maxLength": 100,
                            "nullable": false,
                            "info": {}
                        }
                    }
                }
            },
            "post": {
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "isbn": {
                        "type": "string",
                        "maxLength": 20,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pubYear": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "authorId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "author.id",
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "author_id": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "author.id",
                            "info": {}
                        },
                        "author": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Author"
                            }
                        },
                        "isbn": {
                            "type": "string",
                            "maxLength": 20,
                            "nullable": true,
                            "info": {}
                        },
                        "pub_year": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "info": {}
                        },
                        "title": {
                            "type": "string",
                            "maxLength": 100,
                            "nullable": false,
                            "info": {}
                        }
                    }
                }
            },
            "put": {
                "url": "/books/<int:id>",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "isbn": {
                        "type": "string",
                        "maxLength": 20,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pubYear": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "authorId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "author.id",
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "author_id": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "author.id",
                            "info": {}
                        },
                        "author": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Author"
                            }
                        },
                        "isbn": {
                            "type": "string",
                            "maxLength": 20,
                            "nullable": true,
                            "info": {}
                        },
                        "pub_year": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "info": {}
                        },
                        "title": {
                            "type": "string",
                            "maxLength": 100,
                            "nullable": false,
                            "info": {}
                        }
                    }
                }
            },
            "patch": {
                "url": "/books/<int:id>",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "isbn": {
                        "type": "string",
                        "maxLength": 20,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pubYear": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "authorId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "author.id",
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "author_id": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "author.id",
                            "info": {}
                        },
                        "author": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Author"
                            }
                        },
                        "isbn": {
                            "type": "string",
                            "maxLength": 20,
                            "nullable": true,
                            "info": {}
                        },
                        "pub_year": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "info": {}
                        },
                        "title": {
                            "type": "string",
                            "maxLength": 100,
                            "nullable": false,
                            "info": {}
                        }
                    }
                }
            },
            "delete": {
                "url": "/books/<int:id>",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    }
                },
                "responses": {}
            }
        },
        "table": {
            "Book": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "isbn": {
                        "type": "string",
                        "maxLength": 20,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pub_year": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "author_id": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "author.id",
                        "info": {}
                    },
                    "author": {
                        "readOnly": true,
                        "relationship": {
                            "type": "single",
                            "entity": "Author"
                        }
                    }
                },
                "xml": "Book"
            }
        }
    }

..

With the use of method decorators for authenticated users, a fair number of database tables can be presented via an API with just this vanilla approach.

In the next section we will look at a few tweaks and modifications that can handle more complicated issues.
