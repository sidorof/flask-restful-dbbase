
Flask-RESTful-DBBase documentation
==================================

This package provides datacentric web API resources within the Flask environment. It is a pragmatic approach, applying REST principles. However, there are hooks for converting HTTP methods to RPCs as well. That enables the serialization and validation services to be used, but frees up methods to return whatever is appropriate for your situation if necessary.

The work that goes into carefully defining the data structures in the database can be reused in all the layers out to the front-end application. Flask-RESTful-DBBase evaluates the model definitions and expresses this understanding in resources in the API via introspection. It is used for several functions:

- Data validation and conversion
- Presentation of the return data can be tailored according to your audience
- Meta resources provide documentation functions to the API of capabilities and requirements.
- An awareness that special cases and considerations exist that require modifications beyond just the basics. There are functions for each kind of method that can hit the processing at important points for validation, dataconversion, and message passing.
- It can take advantage of Flask-RESTful method decorators and has functions that can use the information provided by such decorators.

A REST resource can be created as easily as:

.. code-block:: python

    class Book(ModelResource):
        model_class = Book
..

This resource class by default instantiates a URL at:

.. code-block::

    /books
    /books/<int:id>
..
- URLs are pluralized by default, but can be customized, relocated, or replaced completely.
- The primary key(s) are automatically derived from the underlying model.
- Serialization / deserialization, validation and conversion, services flow from introspection of the data model. Specifying output fields is straight-forward and can include / exclude relationship data.
- HTTP methods implemented are GET, POST, PUT, PATCH, and DELETE.
- POSTing parent data may include child data to reduce round trips.
- If a requirement is sufficiently different from the REST API approach, the serialization and validation services can still be used in a non-model resource.


.. toctree::
   :maxdepth: 2

   installation.rst
   user_guide.rst
   app-simple.rst
   app-owner-v1.rst
   app-owner-v2.rst
<<<<<<< HEAD
   app-register.rst
   model-resource.rst
   parent-child-posting.rst
   model-collection-resource.rst
   meta-resource.rst
   limited-method-resources.rst
=======
   parent-child-posting.rst
   resource-classes.rst
>>>>>>> develop
   examples.rst
   api.rst
   testing.rst
   license.rst
   changelog.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
