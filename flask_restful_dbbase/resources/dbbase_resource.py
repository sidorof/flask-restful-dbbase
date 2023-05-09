# flask_restful_dbbase/resources/dbbase_resource.py
""""
This module implements a starting point for model resources.

"""
from os import path
from dateutil.parser import parse
import inflect

from flask_restful import Resource
from dbbase.utils import xlate

from ..doc_utils import MetaDoc


class DBBaseResource(Resource):
    """
    DBBaseResource Class

    This model class implements the base class.

    model_class: a dbbase.Model
    url_prefix: the portion of the path leading up to the resource,
    for example: /api/v2

    url_name: the url_name defaults to a lower case version of the
    the model_class name if left as None, but can have an explicit
    name if necessary.

    serial_fields: if left as None, it uses the serial list from
    the model class. Left as None, it will default to the
    underlying model.

    serial_field_relations: can customize how relationship variables
    are presented in output.

    before_commit/after_commit: These variables are designed to extend
    the capabilities of the methods be enabling a function or
    class to modify the data just prior to commit, or after. By
    using these, it is possible to send data to message queues,
    adjust the data, or otherwise change the data.

    There are expectations of about the functions/classes.

    Format for a before/after function:

    `def myfunc(resource_self, item, status_code):`

    Args:
        resource_self: (obj) : This is the self of the resource.
            This provides access to the resource itself.
        item: (obj) : This is the SQLAlchemy object.
        status_code (int) : If due to the processing that status_code
            should change, you can change it here. Otherwise, simply
            return it.
    Returns:
        item: (obj) : The modified record
        status_code (int) : The possibly altered response status_code

    Example of a Class:

    A class can be used to hold additional data.
    This example shows how a resource can receive a POSTed object, but
    return the job created as a result instead.

    A class requires that a `run` function be implemented with the
    input variables as shown below.

    class JobCreator(object):
        def __init__(self, class_name):
            self.Job = class_name

        def run(self, resource_self, item, status_code):
            # obj_self gives access resource characteristics
            # but not used in this case
            data = item.to_dict(to_camel_case=False)
            job = self.Job()
            job = self.Job(
                owner_id=data['owner_id'],
                model_id=data['id'],
                job_type_id=0,
                status_id=0
            ).save()
            if resource_self.serial_fields is None:
                resource_self.serial_fields = {}
            resource_self.serial_fields['post'] = \
                self.Job.get_serial_fields()

            # job submitted here ->

            status_code = 202
            return job, status_code

    meta_doc: This set of attributes is designed to supplement meta
    information automatically generated. It uses the MetaDoc class
    found in utils.

    """

    model_class = None
    model_name = None
    """
    The string version of the Model class name. This is set
    upon initialization.
    """
    url_prefix = "/"

    url_name = None
    use_date_conversions = False
    """
    use_date_conversions can be used if the database, such as SQlite3 does
    not support the acceptance of string-based dates. Since it takes processing
    time and adherence to a format, it is an optional feature.
    """

    # output params
    serial_fields = None
    serial_field_relations = None

    before_commit = {}
    after_commit = {}

    default_sort = None
    requires_parameter = False
    fields = None

    meta_doc = None

    def __init__(self):
        if self.model_class is None:
            msg = "A model class must be set for this resource to function."
            raise ValueError(msg)
        self.model_name = self.model_class._class()

        super().__init__()

    @classmethod
    def get_key_names(cls, formatted=False):
        """get_key_names

        This function returns column names marked as primary_key.

        Args:
            formatted: (bool) : will return in form [<int:id>]

        Returns:
            key_names (list) : a list of keys is returned
        """
        primaries = []
        for key, value in cls.model_class.__dict__.items():
            if hasattr(value, "expression"):
                if isinstance(value.expression, cls.model_class.db.Column):
                    if value.expression.primary_key:
                        primaries.append(key)

        if formatted:
            keys = []
            for key in primaries:
                keys.append(
                    cls.format_key(
                        key,
                        cls.model_class.db.doc_column(cls.model_class, key)[
                            "type"
                        ],
                    )
                )
        else:
            keys = primaries

        return keys

    @classmethod
    def get_obj_params(cls):
        """get_obj_params

        This is a convenience function for getting documentation
        parameters from the model class.

        Returns:
            (dict) : The object properties of the model class

        """
        return cls.model_class.db.doc_table(cls.model_class)[
            cls.model_class._class()
        ]["properties"]

    @staticmethod
    def format_key(key, key_type):
        """
        This function returns the portion of the URL that embodies the key.

        Args:
            key: (str) : The name of the key field.
            key_type: (str) : Either 'integer' or something else.

        Returns:

            formatted key: (str) : such as <int:id>
        """
        if key_type == "integer":
            return f"<int:{key}>"

        return f"<string:{key}>"

    @classmethod
    def get_urls(cls):
        """get_urls

        This function returns something similar to
            [ {url_prefix}/{this_url}, {url_prefix}/{this_url}/<int:id> ]

        """
        if cls.model_class is None:
            raise ValueError("A model class must be defined")

        urls = [cls.create_url()]

        if not cls.is_collection():
            key_methods = ["get", "put", "patch", "delete"]

            for method in key_methods:
                if hasattr(cls, method):
                    # create a URL with a key
                    keys = cls.get_key_names(formatted=True)
                    keys = "".join(keys)
                    url_with_key = "/".join([urls[0], keys])
                    urls.append(url_with_key)
                    break
        return urls

    @classmethod
    def get_meta(cls, method=None):
        """
        This function returns the settings for the resource.

        Args:
            method: (str : None) : choices are get/post/put/patch/delete.

        Returns:
            meta_data (dict) : A dict with the resource characteristics.
            If a method is preferred, the focus will be narrowed to that
            method.

        The intent of this function is to show relevant information for someone
        interacting with an API.

        """
        if cls.meta_doc is None:
            cls.meta_doc = MetaDoc(resource_class=cls)

        return cls.meta_doc.to_dict(method=method)

    @classmethod
    def is_collection(cls):
        """
        This function returns True if identified as a collection resource.
        """
        # uses max_page_size as a marker
        return hasattr(cls, "max_page_size")

    @staticmethod
    def _all_keys_found(key_names, data):
        if isinstance(key_names, str):
            if key_names in data:
                return True, {key_names: data[key_names]}
        else:
            count = 0
            new_dict = {}
            for key_name in key_names:
                if key_name in data:
                    count += 1
                    new_dict[key_name] = data[key_name]

            if count and count == len(key_names):
                return True, new_dict

        return False, {}

    def _check_key(self, kwargs):
        # these are the kwargs passed in
        # kwargs without ** is intentional
        key_names = self.get_key_names()
        status, kdict = self._all_keys_found(key_names, kwargs)
        if status:
            return kdict

        if len(key_names) == 1:
            key_names = key_names[0]
        raise ValueError(
            f"This method requires the {key_names} in the URL for "
            f"{self.model_name}."
        )

    @classmethod
    def _get_serial_fields(cls, method, with_class=False):
        """_get_serial_fields

        see class description for use

        If with_class a foreign class will be included:
        example:
            model_class = "MlModels"
            serial_fields = {
                "get": ['id, 'model_name']
                "post": {Job: ['id', 'job_type_id']}
            }
        """
        serial_fields = None
        if isinstance(cls.serial_fields, dict):
            if method in cls.serial_fields:
                serial_fields = cls.serial_fields[method]
        else:
            serial_fields = cls.serial_fields

        if isinstance(serial_fields, dict) and not with_class:
            # dict is only used with meta information
            serial_fields = list(serial_fields.values())[0]

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

        # NOTE: think about this one
        # if isinstance(serial_field_relations, dict):
        #     # dict is only used with meta information
        #     serial_field_relations = serial_field_relations.values()[0]

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
                {"message": "Configuration error: missing model_class."},
                500,
            )

    @classmethod
    def create_url(cls):
        """create_url

        Url can come from:
        * url_name resource variable

        but if None
        * snake_case version of class name

        NOTE: figure out flag for use table/classname
        """
        cls._check_config_error()
        if cls.url_name is None:
            # attempt to derive it
            _pluralizer = inflect.engine()
            url_name = xlate(cls.model_class._class(), camel_case=False)
            url_name = _pluralizer.plural((url_name))
            url_name = url_name.replace("_", "-")
        else:
            url_name = cls.url_name

        url_prefix = cls.url_prefix

        return path.join(url_prefix, url_name)

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
        """
        # filtering first
        errors = []
        required = []
        # data = self._remove_unnecessary_data(data)

        # check from standpoint of obj_params
        for col_key, col_params in obj_params.items():
            read_only = col_params.get("readOnly")
            not_relation = "relationship" not in col_params
            if not read_only and not_relation:
                if col_key in data:
                    value = data[col_key]
                    # find reasons to exclude
                    tmp_errors = self._check_numeric_casting(
                        col_key, value, col_params
                    )
                    if tmp_errors:
                        errors.extend(tmp_errors)

                    tmp_errors = self._check_max_text_lengths(
                        col_key, value, col_params
                    )
                    if tmp_errors:
                        errors.extend(tmp_errors)

                    if self.use_date_conversions:
                        dtstatus, value = self._check_date_casting(
                            col_key, value, col_params
                        )

                        if dtstatus:
                            data[col_key] = value
                        else:
                            errors.extend(value)
                else:
                    # is it required
                    if col_params.get("nullable") is False:
                        required.append(col_key)
            else:
                if read_only and col_key in data:
                    del data[col_key]

        if not skip_missing_data:
            if required:
                errors.append({"missing_columns": required})

        if errors:
            return False, errors

        return True, data

    @staticmethod
    def _check_numeric_casting(col_key, value, col_params):
        """_check_numeric_casting

        This function just makes a quick to see if a numeric field
        data, if in string form, can be converted to a number.

        No check is made on integer or float sizes.
        """
        errors = []

        if value is None:
            return errors

        if col_params["type"] in ["integer", "float"]:
            if isinstance(value, str):
                if not value.isnumeric():
                    errors.append(
                        {col_key: f"The value {value} is not a number"}
                    )

        return errors

    @staticmethod
    def _check_max_text_lengths(col_key, value, col_params):
        """_check_max_text_lengths

        This function compares a maximum length, if available with
        the data value.
        """
        errors = []

        max_len = col_params.get("maxLength")

        if max_len and value is not None:
            if len(value.strip()) > max_len:
                errors.append(
                    {
                        col_key: "The data exceeds the maximum length "
                        f"{max_len}"
                    }
                )

        return errors

    @classmethod
    def _check_date_casting(cls, col_key, value, col_params):
        """_check_date_casting

        This function attempts to change a string date to date object.

        Unlike the other checking functions, this function
        does a conversion to an object if possible.
        """
        errors = []

        if value is None:
            return True, value

        if col_params["type"] == "date":
            try:
                value = parse(value).date()
            except Exception as err:
                msg = f"Date error: '{value}': {err}"

                errors.append({col_key: msg})

        elif col_params["type"] == "date-time":
            try:
                value = parse(value)
            except Exception as err:
                msg = f"Date error: '{value}': {err}"

                errors.append({col_key: msg})

        if errors:
            return False, errors
        else:
            return True, value

    def _item_adjust(self, func, item, status_code):
        """
        This function receives a before/after commit
        function, item and default status_code

        Args:
            func: (func | obj) : either a function or an object.
            If it is an object, it must have a method of 'run'.
            item: (obj) : The object that is being worked on
            status_code: (int) : the default status code associated
            with the HTTP method.
        Return:
            (status, result, status_code) : If the status is True, the
            processing will continue normally with `result` being the
            item that is  processed. The status_code can be changed
            or left to the default status code
            If the status is False, the result would be a JSON object that
            is to be returned to the front-end.
        """
        if callable(func):
            output = func(self, item, status_code)

        else:
            output = func.run(self, item, status_code)

        if isinstance(output, tuple) and len(output) == 3:
            return output

        raise ValueError(
            f"function {func.__name__} must output a tuple of (status, "
            "result, status_code)"
        )
