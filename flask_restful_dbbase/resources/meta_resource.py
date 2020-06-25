# flask_restful_dbbase/meta_resource.py
"""
This module implements resource with a purpose of documenting
a model resource.

Assumes a get method.
"""

from os import path
from flask import request
from . import Resource, CollectionModelResource


class MetaResource(Resource):
    """ MetaResource

    This class enables documentation for a model resource.

    **Class variables**:

    resource_class: This is the model resource that you wish to documnent.

    url_prefix: Like with the ModelResource class, this prefix can be used
    to create a url for the documentation.

    url_name: This is the final part of a url for creating a url.
    It defaults to a name of 'meta'.

    Both the url_prefix and url_name come into play only upon initial
    configuration.
    """

    resource_class = None
    """ This is the resource class to be documented """
    url_prefix = "/meta"
    """ This is the default prefix to be used for the URL."""
    url_name = None
    """
    This name can be used to make the default URL for the meta resource.
    """

    def get(self):
        """
        This function is the request.GET method for the meta resource URL.

        Args:
            method: (str) : can specify only a specific method of the resource
            to be documented, such as get or put.

        Returns:
            meta: (json) : The documentation
        """
        method = request.values.get("method", None)

        if method is not None:
            method = method.lower()

        try:
            return self.resource_class.get_meta(method), 200
        except Exception as err:
            msg = err.args[0]

            return {"message": msg}, 400

    @classmethod
    def get_urls(cls):
        """ get_urls

        This function returns a default url for the resource. To keep
        consistency with the get_urls functions in other resources,
        it returns the url in a list, even though there would never be
        more than one.

        The approach enables a code consistent approach when using the
        api.add_resource function.

        Example:

        api.add_resource(BookResource, *BookResource.get_urls())
        api.add_resource(BookCollection, *BookCollection.get_urls())
        api.add_resource(BookMetaResource, *BookMetaResource.get_urls())
        api.add_resource(BookMetaCollection, *BookMetaCollection.get_urls())

        Default URLS:
        /books
        /books/<int:id>
        /meta/books/single
        /meta/books/collection

        Bear in mind that the `get_urls` function is only for
        convenience when adding the resource the api.
        """
        if cls.url_name is None:
            resource_url = cls.resource_class.create_url()
            if resource_url.startswith("/"):
                resource_url = resource_url[1:]
            if issubclass(cls.resource_class, CollectionModelResource):
                url = path.join(cls.url_prefix, resource_url, "collection")
            else:
                url = path.join(cls.url_prefix, resource_url, "single")
        else:
            url = path.join(cls.url_prefix, cls.url_name)

        return [url]
