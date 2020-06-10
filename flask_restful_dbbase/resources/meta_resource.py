# flask_restful_dbbase/meta_resource.py
"""
This module implements resource with a purpose of documenting
a model resource.

Assumes a get method.

"""
from os import path
from flask import request
from flask_restful_dbbase.resources import Resource


class MetaResource(Resource):
    """ MetaResource

    This class enables documentation for a model resource.

    Class variables:
        resource_class: This is the model resource that you wish to documnent.
        url_prefix: Like with the ModelResource class, this prefix can be used
            to create a url for the documentation.
        url_name: This is the final part of a url for creating a url.
            It defaults to a name of 'meta'.

    Both the url_prefix and url_name come into play only upon initial
    configuration.

    Example:
        Create a class Book and BookResource with the class.
        api.add_resource(BookResource, *BookResource.get_urls())

        Would yield paths:
            /book
            /book/<int:id>

        api.add_resource(BookMetaResource, BookMetaResource.get_urls())

        Would yield a path:
            /book/meta

    The traditional form of adding a resource can be used as well.

    Example:
        api.add_resource(BookResource, '/books', /books/<int:id>)
        api.add_resource(BookMetaResource, '/documentation/books')

    """
    resource_class = None
    url_prefix = None
    url_name = 'meta'

    def get(self):

        method = request.values.get('method', None)

        if method is not None:
            method = method.lower()

        try:
            return self.resource_class.get_meta(method), 200
        except Exception as err:
            msg = err.args[0]

            return {"message": msg}, 400


    @classmethod
    def get_urls(cls):

        if cls.url_prefix is None:
            url = path.join(cls.resource_class.create_url(), cls.url_name)
        else:
            url = path.join(url_prefix, cls.url_name)
        return url
