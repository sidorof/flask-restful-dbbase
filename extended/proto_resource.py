# portapi/resources/primary_resources/proto_resource.py
"""
This module implements a starting point for resources.

"""
from os import path
from inspect import signature

from flask_restful import Resource, reqparse, request


class NodeResource(Resource):

    __name__ = 'NodeResource'

    parent_resource = None

    # flask_restful paramters
    method_decorators = None
    parser = None

    # done this way as cleaner way when expressing meta info
    model_class = None
    url_prefix = "/api"
    path_ids = None

    # output params
    serial_list = None
    relation_serial_lists = None

    use_db = True
    default_sort = None
    requires_parameter = False
    fields = None

    # def __init__(self, model_class=None, url_prefix=None, path_ids=None, serial_list=None, relation_serial_lists=None, use_db=True, default_sort=None, requires_parameter=False, fields=None)

    def __init__(self, model_class=None, url_prefix=None, path_ids=None, **kwargs):
        """
        serial_list=None, relation_serial_lists=None, use_db=True, default_sort=None, requires_parameter=False, fields=None
        """
        self.model_class=model_class
        self.url_prefix = url_prefix if not None else mode


    @classmethod
    def get_urls(cls):
        """
        This function tries to build /item and /item/<int:id> for
        creating resources.

        The goal is to make:
        Example:
        [
            '/api/v1/securities/<int:security_id>/dividends',
            '/api/v1/securities/<int:security_id>/dividends/<int:id>'
        ]

        The SecurityMasterResource has
            url_prefix = 'securities/<int:security_id>'
            path_ids = ['security_id']

        Assume that get, if used, would have the unique id to build the url.

        Using introspection, we can select the last variable and glue it on
        the end of the url

        The basis for this is using inspect.signature on the get function.

        Example:
            def get(self, security_id: int, id: int):


        Returns <Signature (self, security_id, id: int)>

        Also, if the get is for a ListResource, it will only have the path ids.
        Example: /api/v1/securities/<int:security_id>/dividends/<int:id>

        Returns list of urls.


        """
        parent_resource = cls.parent_resource
        url_parts = [cls.url_prefix]
        while True:
            if parent_resource is not None:
                url_parts.insert(0, parent_resource.url_prefix)
                parent_resource = parent_resource.parent_resource
            else:
                break

        return '/'.join(url_parts)

    @staticmethod
    def _as_str(val_type):
        if issubclass(val_type, int):
            return 'int'
        elif issubclass(val_type, int):
            return 'str'
        else:
            return 'undefined'

    @classmethod
    def _get_params(cls):

        vlist = signature(getattr(cls, 'get'))
        last_param = list(vlist.parameters.values())[-1]
        lp_type = cls._as_str(last_param.annotation)
        suffix = f'<{lp_type}:{last_param.name}>'
        return suffix

    @classmethod
    def _in_path_ids(cls, name):
       """ _in_path_ids

       This function returns True if param name is in cls.path_ids.
       """
       if cls.path_ids is not None:
           return name in cls.path_ids

    @classmethod
    def display_parser(cls):
        if cls.parser is not None:
            tmp = {
                "bundle_errors": cls.parser.bundle_errors,
                "trim": cls.parser.trim
            }

            tmp['args'] = []
            for arg in cls.parser.args:
                tmp['args'].append(repr(arg).replace("\'", '"'))

            return tmp

    @classmethod
    def get_meta(cls):
        """
        This function returns the settings for the resource.

        """
        tmp = {
            "model_class": cls.model_class,
            "url_prefix": cls.url_prefix,
            'output': {
                "serial_list": cls.serial_list,
                "relation_serial_lists": cls.relation_serial_lists,
            },
            "input": {
                "use_db": cls.use_db,
                "default_sort": cls.default_sort,
                "requires_parameter": cls.requires_parameter,
                "fields": cls.fields,
            }
        }

        tmp["url"] = cls.get_base_url()

        methods = [
            method
            for method in [
                "head",
                "options",
                "get",
                "post",
                "put",
                "pathch",
                "delete",
                "trace",
            ]
            if hasattr(cls, method)
        ]
        tmp["methods"] = methods

        if cls.method_decorators is None:
            tmp['method_decorators'] = None
        elif isinstance(cls.method_decorators, list):
            tmp['method_decorators'] = [func.__name__ for func in cls.method_decorators]
        elif isinstance(cls.method_decorators, dict):
            tmp_md = {}
            for key, value in cls.method_decorators.items():
                tmp_md[key] = [func.__name__ for func in value]
            tmp['method_decorators'] = tmp_md
        else:
            tmp['method_decorators'] = cls.method_decorators

        tmp['parser'] = cls.display_parser()
        return tmp

    @classmethod
    def _get_serial_list(cls, method):
        """_get_serial_list

        see class description for use
        """
        serial_list = None
        if isinstance(cls.serial_list, dict):
            if method in cls.serial_list:
                serial_list = cls.serial_list[method]
        else:
            serial_list = cls.serial_list

        return serial_list

    @classmethod
    def _get_relation_serial_lists(cls, method):
        """_get_relation_serial_lists

        see class description for use
        """
        relation_serial_lists = None
        if isinstance(cls.relation_serial_lists, dict):
            if method in cls.relation_serial_lists:
                relation_serial_lists = cls.relation_serial_lists[method]
        else:
            relation_serial_lists = cls.relation_serial_lists

        return relation_serial_lists

    @classmethod
    def _get_serialization_lists(cls, method):

        return (
            cls._get_serial_list(method),
            cls._get_relation_serial_lists(method),
        )

    @classmethod
    def _check_config_error(cls):
        """_check_config_error

        This function returns a message, response code
        if the model_class has not been configured.
        """
        if cls.model_class is None:
            return (
                {"message": f"Configuration error: missing model_class."},
                500,
            )

    @classmethod
    def create_url(cls):
        cls._check_config_error()

        url_prefix = cls.url_prefix

        url_cls = cls.model_class.__tablename__
        url_cls = url_cls.replace("_", "-")

        return f"{url_prefix}{url_cls}"
