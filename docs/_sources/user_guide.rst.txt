==========
User Guide
==========

------------
Introduction
------------

Flask-RESTful-DBBase creates resources with a helpful set of defaults, but provides numerous fallback positions to customize the resource capabilities to the requirements of the problem.

The capabilities are presented with a few simple apps designed to highlight the features.

- Introduction to the primary classes :class:`~flask_restful_dbbase.resources.ModelResource`, :class:`~flask_restful_dbbase.resources.CollectionModelResource`, and :class:`~flask_restful_dbbase.resources.MetaResource`.
- Simple modification functions that can work in concert with Flask-RESTful `method_decorators` to implement more complex abilities with minimal changes. :ref:`Simple Owner App`
- An example of diverting a post process to a message queue and returning the job data. :ref:`Simple Owner App Revised`
- An example of posting parent data and including child data and saving multiple round trips from the front-end. :ref:`Parent Post - Child Records`
- An example of creating a POST-only resource that diverts output from the REST response to a customized message and response status code. :ref:`Limited Method Resources`

.. include:: app-simple.rst
.. include:: app-owner-v1.rst
.. include:: app-owner-v2.rst
.. include:: parent-child-posting.rst
.. include:: limited-method-resources.rst
