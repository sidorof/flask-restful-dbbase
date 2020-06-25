# flask_restful_dbbase/resources/dbbase_resource.py
""""
This module implements a starting point for model resources.

"""
from os import path
import inflect

from flask_restful import Resource
from dbbase.utils import xlate


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
        item: (obj) : This is SQLAlchemy record.
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

    """

    model_class = None
    model_name = None
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
    def get_key_names(cls, formatted=False):
        """ get_key_names

        This function returns column names marked as primary_key.

        Args:
            formatted: (bool) : will return in form [<int:id>]

        Returns:
            key_names (list) : a list of keys is returned
        """
        columns = cls.model_class.filter_columns(
            column_props=["primary_key", "type"]
        )
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
        keys = cls.get_key_names(formatted=True)
        keys = "".join(keys)
        url_with_id = "/".join([url, keys])

        return [url, url_with_id]

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
        db = cls.model_class.db
        method_list = ["get", "post", "put", "patch", "delete"]
        if method is None:
            doc = {
                "model_class": cls.model_class._class(),
                "url_prefix": cls.url_prefix,
                "url": cls.create_url(),
            }
            doc["methods"] = {}
            # this is done to force order without OrderedDict
            for method in method_list:
                if hasattr(cls, method):
                    doc["methods"][method] = cls._meta_method(method)
            doc["table"] = db.doc_table(cls.model_class)

        else:
            # just the method
            # if method not in method_list:
            # methods = str(cls.model_class.methods).lower()
            # raise ValueError(
            # f'Support methods for this resource are: {methods}')
            if hasattr(cls, method):
                doc = {"method": {method: cls._meta_method(method)}}
            else:
                raise ValueError(
                    f"Method '{method}' is not found for this resource"
                )
        return doc

    @classmethod
    def is_collection(cls):
        """
        This function returns True if identified as a collection resource.
        """
        # uses max_page_size as a marker
        return hasattr(cls, "max_page_size")

    @classmethod
    def _meta_method(cls, method):
        """
        This function builds the dict meta data object for a specific method.

        Args:
            method: (str) : The method to be documented.
        """
        db = cls.model_class.db

        method_dict = {}

        if method in ["get", "put", "patch", "delete"]:
            # NOTE: need to identify a collection resource here
            if cls.is_collection():
                method_dict["url"] = cls.get_urls()[0]
            else:
                method_dict["url"] = cls.get_urls()[1]

        method_dict["requirements"] = cls._meta_method_decorators(method)
        if method in ["get", "delete"]:
            if cls.is_collection():
                method_dict["query_string"] = cls.model_class.filter_columns(
                    column_props=["!readOnly"], to_camel_case=True,
                )
            else:
                keys = cls.get_key_names()
                if len(keys) > 1:
                    method_dict["input"] = [
                        dict([[key, db.doc_column(cls.model_class, key)]])
                        for key in keys
                    ]
                else:
                    key = keys[0]
                    method_dict["input"] = {
                        key: db.doc_column(cls.model_class, key)
                    }

        else:
            # select all columns that are not read only
            method_dict["input"] = cls.model_class.filter_columns(
                column_props=["!readOnly"], to_camel_case=True,
            )

        method_dict["responses"] = cls._meta_method_response(method)
        return method_dict

    @classmethod
    def _meta_method_decorators(cls, method):
        # method decorators go in as requirements

        requirements = []
        if isinstance(cls.method_decorators, list):
            requirements = [func.__name__ for func in cls.method_decorators]
        elif isinstance(cls.method_decorators, dict):
            if method in cls.method_decorators:
                requirements = [
                    func.__name__ for func in cls.method_decorators[method]
                ]

        return requirements

    @classmethod
    def _meta_method_response(cls, method):
        """ _meta_method_response

        The real way to do this:

        NOTE: Develop a resolved list of serial fields and serial field
        relations. Then pass both a doc function and use the
        serialization routines to follow relationships to the source.
        This would capture the detail associated with the relationships
        as well. Part of the issue is that related serializations work
        well with instantiated data, because the related classes are
        available when using to_dict(). However, the related classes
        within a class method might need to plumb metadata(?) to get
        all the pieces.
        """
        db = cls.model_class.db

        outputs = {}

        if method != "delete":
            doc = db.doc_table(
                cls.model_class,
                serial_fields=cls._get_serial_fields(method),
                serial_field_relations=cls._get_serial_field_relations(method),
            )[cls.model_class._class()]
            outputs["fields"] = doc["properties"]

            # NOTE: here is where the default sort would go for collections

        return outputs

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

        # if serial_fields is None:
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
                {"message": "Configuration error: missing model_class."},
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
            _pluralizer = inflect.engine()
            url_name = xlate(cls.model_class._class(), camel_case=False)
            url_name = _pluralizer.plural((url_name))
            url_name = url_name.replace("_", "-")
        else:
            url_name = cls.url_name

        url_prefix = cls.url_prefix

        return path.join(url_prefix, url_name)

    def screen_data(self, data, skip_missing_data=False):
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
        data = self._remove_unnecessary_data(data)

        if not skip_missing_data:
            # check required first
            missing_columns = self._missing_required(data)
            if missing_columns:
                errors.append(missing_columns)
        # check lengths of text
        tmp_errors = self._check_max_text_lengths(data)

        if tmp_errors:
            errors.extend(tmp_errors)

        # check for numerics -- skipping check integer size for now
        tmp_errors = self._check_numeric_casting(data)
        if tmp_errors:
            errors.extend(tmp_errors)

        if errors:
            return False, errors

        return True, data

    @classmethod
    def _check_numeric_casting(cls, data):
        """ _check_numeric_casting

        This function just makes a quick to see if a numeric field
        data, if in string form, can be converted to a number.

        No check is made on integer or float sizes.
        """
        errors = []
        column_types = cls.model_class.filter_columns(
            column_props=["type"], only_props=True
        )

        for field, value in data.items():
            if "type" in column_types[field]:
                if column_types[field]["type"] in ["integer", "float"]:
                    if isinstance(value, str):
                        if not value.isnumeric():
                            errors.append(
                                {field: f"The value {value} is not a number"}
                            )
        return errors

    @classmethod
    def _check_max_text_lengths(cls, data):
        """ _check_max_text_lengths

        This function compares a maximum length, if available with
        the data value.
        """
        columns = cls.model_class.filter_columns(
            column_props=["maxLength"], only_props=True
        )
        errors = []
        for column, col_length in columns.items():
            max_len = col_length["maxLength"]
            if column in data:
                value = data[column]

                if len(value.strip()) > max_len:
                    errors.append(
                        {
                            column: "The data exceeds the maximum length "
                            f"{max_len}"
                        }
                    )
        return errors

    @classmethod
    def _remove_unnecessary_data(cls, data):
        """ _remove_unnecessary_data

        This function removes any fields that are unnecessary.

        """
        column_types = cls.model_class.filter_columns(
            column_props=["!readOnly"], only_props=True
        )
        return dict(
            [
                (field, value)
                for field, value in data.items()
                if field in column_types
            ]
        )

    @classmethod
    def _missing_required(cls, data):
        """ _missing_required

        This function reports required fields that are missing data.
        """
        # NOTE: filtering needs improvement, includes relationships
        #       this is due to no nullable in relationship
        requireds = cls.model_class.filter_columns(
            column_props=["!nullable"], only_props=True
        )
        missing_columns = []
        for column in requireds.keys():
            if "nullable" in requireds[column]:
                if column not in data:
                    missing_columns.append(column)
        if missing_columns:
            return {"missing_columns": missing_columns}

        return None
