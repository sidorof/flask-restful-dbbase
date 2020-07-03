
Flask-RESTful-DBBase documentation
==================================

This package provides datacentric Web API resources within the Flask environment.

The work that goes into carefully defining the data structures in the database can be reused in all the layers out to the front-end application. Flask-RESTful-DBBase evaluates the model definitions and expresses this understanding in resources in the API via introspection. It is used for several functions:

- Data validation and conversion
- Presentation of the return data, which can be tailored according to your audience
- A method of communcation of the capabilities and requirements of your API through the use of meta resources
- An awareness that special cases and considerations exist that require modifications beyond just the basics. There are functions for each kind of method that can hit the processing at important points for validation, dataconversion, and message passing.
- It can take advantage of Flask-RESTful method decorators and has functions that can use the information provided by such decorators.


.. toctree::
   :maxdepth: 3

   installation.rst
   user_guide.rst
   app-owner-v1.rst
   app-owner-v2.rst
   model-resource.rst
   parent-child-posting.rst
   model-collection-resource.rst
   meta-resource.rst
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
