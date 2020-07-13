# flask_restful_dbbase/generator.py
"""
This module implements a technique for creating resources with specific
methods.

A customized resource can be created from a resource, but with some
of the default HTTP methods removed, but with customized resource
modifications applied to make a unique resource.
"""
from flask_restful_dbbase.resources import DBBaseResource


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
            are set in place last, so it is here that additional
            customization of the new resource can be made.

    Returns:
        (obj) : The new resource class
    """
    params = {}
    if model_class is not None:
        params["model_class"] = model_class
    if url_prefix is not None:
        params["url_prefix"] = url_prefix
    if url_prefix is not None:
        params["url_name"] = url_name

    # accumulate changes from subclassing
    # follow subclassing order
    class_dict = {}
    idx = resource_class.mro().index(DBBaseResource)
    for i in range(idx - 1, -1, -1):
        cls = resource_class.mro()[i]
        class_dict.update(cls.__dict__)
    if methods is not None:
        # create stop list
        stop_method_list = ["get", "post", "put", "patch", "delete"]
        for method in methods:
            if method in stop_method_list:
                stop_method_list.remove(method)

        for method in stop_method_list:
            del class_dict[method]
            del class_dict[f"process_{method}_input"]
        class_dict["methods"] = set([method.upper() for method in methods])

    class_dict.update(params)

    if class_vars is not None:
        class_dict.update(class_vars)

    new_class = type(name, (DBBaseResource,), class_dict,)

    # required model check
    if new_class.model_class is None:
        raise ValueError("A model class must be defined")

    return new_class
