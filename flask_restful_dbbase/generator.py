# flask_restful_dbbase/generator.py
"""
This module implements a technique for creating resources on the fly.
"""
import logging
from . import db
from . import api
from . import ModelResource


def create_resources(
        resource_class,
        model_classes=None,
        methods=None,
        url_prefix=None,
        echo=True,
        exclude_class_part='Model'
        ):
    """
    This function creates model resource classes from a base resource class.

    Create subclassed resource that has features needed
        Flask-RESTful features such as:
            method_decorators such as
            example:
            method_decorators = {
                "get": [jwt_required],
                "post": [staff_required, jwt_required],
                "put": [staff_required, jwt_required],
                "delete": [staff_required, jwt_required],
            }

        Flask-RESTful-DBBase features
            url_prefix ex. /api/v2


    This process will derive the path name from hints from the model class name
        for example, it could use
            the model class name
                ex. UserGroup -> /api/v2/user-group
            the model class __tablename__
                ex.user_groups -> /api/v2/user-groups

    Specify the methods that it will use:
        if methods is not None
            only the methods listed will be implemented in the set of resources

    """
    resource_list = []
    for cls in class_list:
        url_prefix = make_name(cls)
        name = f"{cls._class()}ListResource"
        new_list = type(
            name,
            (SingleListResource,),
            {"model_class": cls, "url_prefix": url_prefix},
        )
        # resource_list.append([new_list, make_url(cls, "mult")])
        resource_list.append(new_list)

        name = f"{cls._class()}Resource"
        new_single = type(
            name,
            (SingleResource,),
            {"model_class": cls, "url_prefix": url_prefix},
        )

        # resource_list.append([new_single, make_url(cls, "single")])
        resource_list.append(new_single)
