# flask_restful_dbbase/generator.py
"""
This module implements a technique for creating resources on the fly.
"""
from datetime import date
from flask_restful_dbbase.resources import (
    DBBaseResource,
    CollectionModelResource,
    ModelResource
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

    new_dict = {
        "model_class": model_class,
        "url_prefix": url_prefix,
        "url_name": url_name,
    }

    if methods is None:
        methods = ["get", "post", "put", "patch", "delete"]
    for method in methods:
        new_dict[method] = getattr(resource_class, method)
        process_function = f"process_{method}_input"
        new_dict[process_function] = getattr(resource_class, process_function)

    # DBBaseResource class variables
    dbbase_vars = [
        "method_decorators",
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

    new_class = type(name, (DBBaseResource,), new_dict,)

    if class_vars is not None:
        for key, value in class_vars.items():
            setattr(new_class, key, value)

    return new_class
