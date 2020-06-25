==============
Meta Resources
==============

Meta resources can help document API model resources, covering input variables, output variables and a thorough description of the underlying model that informs the resource.

Creation
--------

An example of creating a meta resource is as follows:

First, you will need either a ModelResource or a CollectionModelResource for documentation. For example the BookResource used as an example in other areas of this documentation.

A minimal example:

.. code-block:: python

    class BookMetaResource(MetaModelResource):
        resource_class = BookResource

    class BookMetaCollection(MetaModelResource):
        resource_class = BookResource

..

Two resources have been created. The default URLs created for these two resources are:

.. code-block:: python

    /meta/books/single
    /meta/books/collection
..

As with the :ref:`Collection Resources`, there is a single URL created encased in a list for consistency with the model resources.


GET Method
----------
The meta resource just uses a GET method for the source of information. Because of the volume of information produced, there is an option for limiting the query to a single method, such as:

    `/meta/books/single?method=post`

