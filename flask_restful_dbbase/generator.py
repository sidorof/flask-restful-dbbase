# flask_restful_dbbase/generator.py
"""
This module implements a technique for creating resources on the fly.

There are two main use cases for this:
* A list of model classes can be iterated through the generator to
create a set of resources of things like common method decorators.
* A customized resource can be created from a resource, but with some
of the default HTTP methods removed, but with customized resource
modifications applied to make a unique resource.
"""
from datetime import date
from flask_restful_dbbase.resources import (
    DBBaseResource,
    CollectionModelResource,
    ModelResource,
    MetaResource,
)


def create_resource(
    name,
    resource_class,
    model_class=None,
    methods=None,
    url_prefix=None,
    url_name=None,
    class_vars=None,
):
    """
    This function creates a resource based on a source model class
    and a seed resource.

    Args:
        name: (str) : This will be the name stored with the new
        class.

        resource_class: (obj) : This is the ModelResource class that
        will be used as the basis of the new class.

        methods: (list) : This the list of HTTP methods that should
        be transferred to the new class.

        url_prefix: (str) : This is url_prefix that can be used in place of
        the default url_prefix that comes with the resource class.
        url_name: (str) : This the url_name that can be used in place
        of the default url_name that comes with the resource.
        class_vars: (dict) : This is a dictionary of variables and
        values that will be transferred to the new resource. These
        are set in place last, so it is here that customization of
        the new resource is made.

    Returns:
        (obj) : The new resource class
    """
    new_dict = {
        "model_class": model_class,
        "url_prefix": url_prefix,
        "url_name": url_name,
    }

    if methods is None:
        methods = resource_class.methods
    for method in methods:
        method = method.lower()
        new_dict[method] = getattr(resource_class, method)
        process_function = f"process_{method}_input"
        new_dict[process_function] = getattr(resource_class, process_function)

    # DBBaseResource class variables
    dbbase_vars = [
        "method_decorators",
        "url_prefix",
        "url_name",
        "serial_fields",
        "serial_field_relations",
        "default_sort",
        "requires_parameter",
        "fields",
        "use_date_conversions",
        "before_commit",
        "after_commit",
    ]

    for cls_var in dbbase_vars:
        new_dict[cls_var] = getattr(resource_class, cls_var)

    # Specific CollectionResource variables
    if resource_class.is_collection():
        new_dict["max_page_size"] = resource_class.max_page_size

    new_class = type(name, (DBBaseResource,), new_dict,)

    if class_vars is not None:
        for key, value in class_vars.items():
            setattr(new_class, key, value)

    # required model check
    if new_class.model_class is None:
        raise ValueError("A model class must be defined")

    return new_class


def create_meta_resource(
    name, resource_class, url_prefix="meta", class_vars=None):
    """
    This function creates a meta resource based on a source model
    class and a seed resource.

    Args:
        name: (str) : This will be the name stored with the new
        class.

        resource_class: (obj) : This is the ModelResource class that
        will be used as the basis of the new meta resource.

        url_prefix: (str) : This is url_prefix that can be used in place of
        the default url_prefix that comes with the resource class.

        class_vars: (dict) : This is a dictionary of variables and
        values that will be transferred to the new meta resource. These
        are set in place last, so it is here that customization of
        the new resource is made.

    Returns:
        (obj) : The new resource class

    This function assumes that only a get method is supported.
    """
    new_dict = {
        "url_prefix": url_prefix,
        "get": getattr(resource_class, "get"),
        "resource_class": resource_class,
    }

    # DBBaseResource class variables
    dbbase_vars = [
        "method_decorators",
    ]

    for cls_var in dbbase_vars:
        new_dict[cls_var] = getattr(resource_class, cls_var)

    new_class = type(name, (MetaResource,), new_dict,)

    if class_vars is not None:
        for key, value in class_vars.items():
            setattr(new_class, key, value)

    return new_class
