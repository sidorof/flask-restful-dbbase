# flask_restful/resources/dbbase_resource.py
""""
This module implements a starting point for model resources.

"""
from os import path
from inspect import signature

from flask_restful import Resource, reqparse, request
from dbbase.utils import xlate
from ..utils import check_existing_id, check_mismatch_ids


class DBBaseResource(Resource):
    """
    DBBaseResource Class

    This model class implements the base class.

    model_class: a dbbase.Model
    url_prefix: the portion of the path leading up to the resource
        For example: /api/v2

    url_name: the url_name defaults to a lower case version of the
        the model_class name if left as None, but can have an
        explicit name if necessary.

    serial_fields: if left as None, it uses the serial list from
        the model class. However, it can be a list of field names
        or



    """

    # done this way as cleaner way when expressing meta info
    model_class = None
    url_prefix = "/"
    url_name = None

    # output params
    serial_fields = None
    serial_field_relations = None

    default_sort = None
    requires_parameter = False
    fields = None

    before_commit = {}
    after_commit = {}

    @classmethod
    def get_key(cls, formatted=False):
        """ get_key

        This function returns column names marked as primary_key.

        Args:
            formatted: (bool) : will return in form <int:id>

        Returns:
            key (str | list) : In the case of multiple primary keys
                a list of keys is returned.
        """
        columns = cls.get_obj_params(column_props=["primary_key", "type"])
        if formatted:
            keys = []
            for key, value in columns.items():
                if "primary_key" in value:
                    keys.append(cls.format_key(key, value["type"]))
        else:
            keys = [
                key
                for key, value in columns.items()
                if value.get("primary_key")
            ]

        return keys if len(keys) > 1 else keys[0]

    @classmethod
    def get_obj_params(cls, column_props=None):
        """get_obj_params

        This is a convenience function for getting documentation
        parameters from the model class.

        Args:
            column_props: (None | list) : filtered properties

        Returns:
            (dict) : The object properties of the model class
        """
        return cls.model_class.db.doc_table(
            cls.model_class, column_props=column_props
        )[cls.model_class._class()]["properties"]

    @staticmethod
    def format_key(key, key_type):
        if key_type == "integer":
            return f"<int:{key}>"

        return f"<string:{key}>"

    @classmethod
    def get_urls(cls):
        """get_urls

        This function returns something similar to
        [
            {url_prefix}/{this_url},
            {url_prefix}/{this_url}/<int:id>
        ]

        """
        if cls.model_class is None:
            raise ValueError("A model class must be defined")

        url = cls.create_url()
        keys = cls.get_key(formatted=True)
        if isinstance(keys, list):
            keys = "".join(keys)
        url_with_id = "/".join([url, keys])

        return [url, url_with_id]

    @classmethod
    def get_meta(cls):
        """
        This function returns the settings for the resource.

        """
        tmp = {
            "model_class": cls.model_class,
            "url_prefix": cls.url_prefix,
            "output": {
                "serial_fields": cls.serial_fields,
                "serial_field_relations": cls.serial_field_relations,
            },
            "input": {
                "use_db": cls.use_db,
                "default_sort": cls.default_sort,
                "requires_parameter": cls.requires_parameter,
                "fields": cls.fields,
            },
        }

        tmp["url"] = cls.get_base_url()

        methods = [
            method
            for method in [
                # "head",
                # "options",
                "get",
                "post",
                "put",
                "patch",
                "delete",
            ]
            if hasattr(cls, method)
        ]
        tmp["methods"] = methods

        if cls.method_decorators is None:
            tmp["method_decorators"] = None
        elif isinstance(cls.method_decorators, list):
            tmp["method_decorators"] = [
                func.__name__ for func in cls.method_decorators
            ]
        elif isinstance(cls.method_decorators, dict):
            tmp_md = {}
            for key, value in cls.method_decorators.items():
                tmp_md[key] = [func.__name__ for func in value]
            tmp["method_decorators"] = tmp_md
        else:
            tmp["method_decorators"] = cls.method_decorators

        tmp["parser"] = cls.display_parser()
        return tmp

    @classmethod
    def _check_key(cls, kwargs):
        # these are the kwargs passed in
        # kwargs without ** is intentional
        key_name = cls.get_key()
        if key_name not in kwargs:
            name = cls.model_class._class()
            raise ValueError(
                f"No key for {name} given. "
                "This is a configuration problem in the url for "
                "this kind of method."
            )
        return key_name, kwargs[key_name]

    @classmethod
    def _get_serial_fields(cls, method):
        """_get_serial_fields

        see class description for use
        """
        serial_fields = None
        if isinstance(cls.serial_fields, dict):
            if method in cls.serial_fields:
                serial_fields = cls.serial_fields[method]
        else:
            serial_fields = cls.serial_fields

        #if serial_fields is None:
        #    serial_fields = cls.model_class.get_serial_fields()

        return serial_fields

    @classmethod
    def _get_serial_field_relations(cls, method):
        """_get_serial_field_relations

        see class description for use
        These are handled differently than serial lists because they are
        not subject to the filtering through stop list on the model class.
        """
        serial_field_relations = None
        if isinstance(cls.serial_field_relations, dict):
            if method in cls.serial_field_relations:
                serial_field_relations = cls.serial_field_relations[method]
        else:
            serial_field_relations = cls.serial_field_relations

        if serial_field_relations is None:
            serial_field_relations = cls.model_class.SERIAL_FIELD_RELATIONS

        return serial_field_relations

    @classmethod
    def _get_serializations(cls, method):

        return (
            cls._get_serial_fields(method),
            cls._get_serial_field_relations(method),
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
        """ create_url

        Url can come from:
        * url_name resource variable

        but if None
        * snake_case version of class name

        NOTE: figure out flag for use table/classname
        """

        cls._check_config_error()
        if cls.url_name is None:
            # attempt to derive it
            url_name = xlate(cls.model_class._class(), camel_case=False)
            url_name = url_name.replace("_", "-")
        else:
            url_name = cls.url_name

        url_prefix = cls.url_prefix

        url = path.join(url_prefix, url_name)
        return f"{url}"

    def screen_data(self, data, obj_params, skip_missing_data=False):
        """
        Assumes data is deserialized

        This function screens data from a few parameters, missing data,
        unneeded fields in data, excessive string lengths, improper numbers.

        Note that this function does not exhaustively determine the
        problem. It ends on first failure.

        Args:
            data: (dict) : incoming data
            obj_params: (dict) : table parameters
            skip_missing_data : (bool) : Flag to check for all for record

        Returns:
            status: (bool) : True, Successful screening
            msg : (None : dict) : description of the problem

        Each test for bad data outputs a status of True, None for each
        successful test. Unsuccessful tests add the problem to an error
        list to be returned at the end. That way, there is a relatively
        complete list of the problems encountered.

        Standard format for list of errors:

        {"type_of_error": [fields]}
            or
        {"type_of_error": [field: {nature of the error},]}

        """
        # filtering first
        errors = []
        obj_params = self._exclude_read_only(obj_params)
        data = self._remove_unnecessary_data(data, obj_params)

        if not skip_missing_data:
            required = self._get_required(obj_params)

            # check required first
            missing_columns = self._missing_required(data, required)

            if missing_columns:
                errors.append(missing_columns)

        # check lengths of text
        tmp_errors = self._check_max_text_lengths(data, obj_params)

        if tmp_errors:
            errors.extend(tmp_errors)

        # check for numerics -- skipping check integer size for now
        tmp_errors = self._check_numeric_casting(data, obj_params)
        if tmp_errors:
            errors.extend(tmp_errors)

        if errors:
            return False, errors

        return True, data

    @staticmethod
    def _check_numeric_casting(data, obj_params):
        """ _check_numeric_casting

        This function just makes a quick to see if a numeric field
        data, if in string form, can be converted to a number.

        No check is made on integer or float sizes.
        """
        errors = []
        for field, value in data.items():
            if "type" in obj_params[field]:
                if obj_params[field]["type"] in ["integer", "float"]:
                    if isinstance(value, str):
                        if not value.isnumeric():
                            errors.append(
                                {field: f"The value {value} is not a number"}
                            )
        return errors

    @staticmethod
    def _check_max_text_lengths(data, obj_params):
        """ _check_max_text_lengths

        This function compares a maximum length, if available with
        the data value.
        """
        errors = []
        for field, value in data.items():
            if "maxLength" in obj_params[field]:
                if len(value.strip()) > obj_params[field]["maxLength"]:
                    max_len = obj_params[field]["maxLength"]

                    errors.append(
                        {
                            field: "The data exceeds the maximum length "
                            f"{max_len}"
                        }
                    )

        return errors

    @staticmethod
    def _remove_unnecessary_data(data, obj_params):
        """ _remove_unnecessary_data

        This function removes any fields that are unnecessary.
        It is assumed that obj_params has been purged of read only
        fields first.
        """
        return dict(
            [
                (field, value)
                for field, value in data.items()
                if field in obj_params
            ]
        )

    @staticmethod
    def _missing_required(data, required):
        """ _missing_required

        This function reports required fields that are missing data.
        """
        missing_columns = []
        for column in required:
            if column not in data:
                missing_columns.append(column)

        if missing_columns:
            return {"missing_columns": missing_columns}

        return None

    @staticmethod
    def _exclude_read_only(obj_params):
        """_exclude_read_only

        This function filters out read only fields from obj_params.

        Args:
            obj_params: (dict) : the properties for a table
        """
        obj_params = dict(
            [
                (column, value)
                for column, value in obj_params.items()
                if "readOnly" not in value
            ]
        )
        return obj_params

    @staticmethod
    def _get_required(obj_params):
        """_get_required

        This function makes a list of the columns that are required.

        Args:
            obj_params: (dict) : the properties for a table
        """
        return [
            column
            for column, values in obj_params.items()
            if values.get("nullable") is False
        ]
