==========
User Guide
==========

------------
Introduction
------------
This package provides datacentric resources within the Flask environment.
The packages that Flask-RESTful-DBBase use are:


* Flask-RESTful for the resource models and API
* SQLAlchemy for communcation to the database
* Flask-SQLAlchemy for sessions, queries and integration with SQLAlchemy within the Flask ecosystem
* DBBase for enhanced Model classes serialization and validation services. In addition, model classes can use the same code when used outside of Flask.

The work that goes into carefully defining the data structures in the database can be reused in all the layers out to the front-end application. Flask-RESTful-DBBase evaluates the model definitions and expresses this understanding in resources in the API via introspection. It is used for several functions:

- Data validation and conversion
- Presentation of the return data, which can be tailored according to your audience
- A method of communcation of the capabilities and requirements of your API through the use of meta resources.
- An awareness that special cases and considerations exist that require modifications beyond just the basics. There are functions for each kind of method that can hit the processing at important points for validation, dataconversion, and message passing.
- It can take advantage of Flask-RESTful method decorators and has functions that can use the information provide by such decorators.


.. include:: app-simple.rst

.. include:: app-owner-v1.rst
