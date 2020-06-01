==========
User Guide
==========

**Flask-Restful-DBBase** leverages SQLAlchemy database models by in
------------
Introduction
------------



-------------
A Minimal API
-------------

A minimal Flask-RESTful-DBBase API looks like this:


.. code-block:: python

    from flask import Flask
    from flask_restful_extended import ModelResource, Api

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(HelloWorld, '/')

    if __name__ == '__main__':
        app.run(debug=True)

..



Getting a database model set correctly with all the constraints, controls and considerations as to how data will be stored now and into the future can be a fair amount of effort. Then, in order to use the database with an API, there is work defining the schema handling variables in and out of the API. This package attempts to reduce the amount of duplication of work and save time.

**Flask-Restful-DBBase** is data-centric. The data is mostly defined in the database, and it makes sense to leverage that effort that has already been done

Using the Python library, `dbbase` to define the models we can use the outputs from those models to power the REST API. Data serialized from the models can be set at the class level to control the data expressed or on the fly. Relationship data can be included, excluded or shaped for specific fields as well. Because of those features, the data can be passed onto resources easily.

There are many ways to use resources. In the following we will look at some hypotheticals to see how the ModelResource can be used in each situation. We will start with a perfect world scenario. Then we look at some fall-back positions as the real world intrudes. Everyone has opinions on naming, formatting,

Steps
-----
*   Start with a simple scenario
*   Create some models to use: Authors and Books
*   Use the models to create resources with default values
*   Examine the data elements that is available from creating the resources
    * Default URLs that are created
    * Document dictionaries for each model
*   Create some records
*   Examine the data expressed


As a working example, let us create a library. The library will hold books, and those books are written by authors. These are models created using dbbase. It will look familiar to those who use Flask-SQLAlchemy

.. code-block:: python

    class Author(db.Model):
        __tablename__ = 'authors'

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)

        def full_name(self):
            return f"{self.first_name} {self.last_name}"

        books = db.relationship(
            "Book", backref="author", lazy="joined"
        )


    class Book(db.Model):
        __tablename__ = 'books'

        id = db.Column(db.Integer, primary_key=True)
        isbn = db.Column(db.String(10), nullable=True)
        title = db.Column(db.String(100), nullable=False)
        pub_date = db.Column(db.Date, nullable=False)
        author_id = db.Column(
            db.Integer, db.ForeignKey('authors.id'), nullable=False)

..

----------------------
Perfect World Scenario
----------------------

In a perfect world, the information gleaned from the Model definition satisfies all requirements.

    `api.create_resources(models=[Book, Author])`

This would result in urls:

.. code-block::

    /author
    /author/<int:id>
    /book
    /book/<int:id>

..

The object properties available for front-end use are:

.. code-block:: json

    {
        "definitions": {
            "Author": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": false,
                        "info": {}
                    },
                    "firstName": {
                        "type": "string",
                        "maxLength": 50,
                        "nullable": false,
                        "info": {}
                    },
                    "lastName": {
                        "type": "string",
                        "maxLength": 50,
                        "nullable": false,
                        "info": {}
                    },
                    "fullName": {
                        "readOnly": true
                    },
                    "books": {
                        "readOnly": true,
                        "relationship": {
                            "type": "list",
                            "entity": "Book"
                        }
                    }
                },
                "xml": "Author"
            },
            "Book": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": false,
                        "info": {}
                    },
                    "isbn": {
                        "type": "string",
                        "maxLength": 10,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pubDate": {
                        "type": "date",
                        "nullable": false,
                        "info": {}
                    },
                    "authorId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "authors.id",
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

* The primary key for the table is automatically identified by the model for get/put/patch/delete
* Incoming data can be effectively evaluated for the requirements for updating the database
* Read-only data is filtered automatically. This enables an instance where a `get` pulls a record which includes non-database information as well. That means that the front-end does not need to screen out the unneeded data on a return trip for an update.
* Response data uses the default serial/relationship data sent to the front end.
* Queries for collection data can use the default variables for data selection
* The url for the resource can be used as the basis for the path name

Given the above, we can create a sample author and book.

.. code-block:: python

    author = Author(first_name='Geoffrey', last_name='Cooper').save()
    book = Book(
        isbn='0-87893-214-3',
        title="The Cell: A Molecular Approach, 3rd edition",
        pub_year=2004,
        author_id=author.id
    ).save()

..

If we request the book from `/book/1`, we receive:

.. code-block:: json

    {
        "id": 1,
        "isbn": "0-87893-214-3",
        "title": "The Cell: A Molecular Approach, 3rd edition",
        "pubYear": 2004,
        "authorId": 1,
        "author": {
            "fullName": "Geoffrey Cooper",
            "id": 1,
            "firstName": "Geoffrey",
            "lastName": "Cooper"
        }
    }

..

if we request the author from `/author/1`, we receive:

.. code-block:: json

    {
        "id": 1,
        "firstName": "Geoffrey",
        "lastName": "Cooper",
        "fullName": "Geoffrey Cooper",
        "books": [
            {
                "pubYear": 2004,
                "id": 1,
                "title": "The Cell: A Molecular Approach, 3rd edition",
                "isbn": "0-87893-214-3",
                "authorId": 1
            }
        ]
    }

..


* GET
    Request:
    The primary key is identified and used
    as the basis for selecting the data.

    Response:
    The default serial list of variables fits the needs for front end use.

* POST
    Request:
    Query strings, form data, JSON are filtered for incompatible data
    Read-only data is automatically excluded

    Response:
    The default serial list of variables fits the needs for front end use.

* PUT
    Request:
    The primary key is identified and used
    Query strings, form data, JSON are filtered for incompatible data
    Read-only data is automatically excluded

    Response:
    The default serial list of variables fits the needs for front end use.

* PATCH


* DELETE

Problems to be solved


/api/v1/libraries/<int:id>/books/<int:id>  since book has a unique id, no need for library
/api/books/<int:id>

-------------------------------------
/libraries                          libraries collection
/libraries/<int:id>                 library document
/libraries/<int:id>/books           library books collection

/books                              books collection
/book/<int:id>                      book document





















