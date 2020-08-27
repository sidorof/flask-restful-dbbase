# flask_restful_dbbase/utils.py
"""
This module implements utilities.
"""
from dbbase.utils import xlate


class MetaDoc(object):
    """
    This class provides a scaffolding for holding documentation
    used when generating meta documents.

    The goal of a meta document is to provide a standard way to communicate
    the features of the backend API to frontend users.

    Resource header:

        model_class
        url_prefix
        base_url
        requirements

    Resource methods:
        single: get/post/put/patch/delete
            input
            input_modifier
            before_commit  (if applicable)
            after_commit   (if applicable)
            responses      (if applicable)

        collection: get
            query
            input_modifier

    Args:
        resource_class: (obj) : The resource documented
        requirements: (str) : The input requirements documented
        methods: (list|dict) : a list or dict of methods that have
            special requirements. Leaving None would mean the default
            documentation.

    """

    all_methods = ("get", "post", "put", "patch", "delete")

    def __init__(
        self, resource_class, requirements=None, methods=None,
    ):
        self.resource_class = resource_class
        self.model_class = resource_class.model_class._class()
        self.url_prefix = resource_class.url_prefix
        self.base_url = resource_class.create_url()
        if methods:
            if isinstance(methods, dict):
                self.methods = methods
            elif isinstance(methods, list):
                # for convenience
                self.methods = {}
                for method in methods:
                    self.methods[method.method] = method
            else:
                raise ValueError("methods must be a dictionary")
        else:
            self.methods = {}

        self.table = None

    def to_dict(self, method=None):
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
        model_class = self.resource_class.model_class
        db = model_class.db

        doc = {}
        attr_list = [
            "model_class",
            "url_prefix",
            "base_url",
            "table",
        ]

        # header keys to camel_case
        for attr in attr_list:
            value = getattr(self, attr)
            if value:
                doc[xlate(attr, camel_case=True)] = value

        self.add_methods(doc, method=method)

        doc["table"] = db.doc_table(model_class)

        return doc

    def add_methods(self, doc, method):
        doc.setdefault("methods", {})
        if method is None:
            for tmp_method in self.all_methods:
                if hasattr(self.resource_class, tmp_method):
                    if tmp_method in self.methods:
                        method_dict = self.methods[tmp_method].to_dict(self)
                        doc["methods"][tmp_method] = method_dict
                    else:
                        doc["methods"][tmp_method] = MethodDoc(
                            tmp_method
                        ).to_dict(self)

        else:
            # check for valid method first
            if not hasattr(self.resource_class, method):
                raise ValueError(
                    f"Method '{method}' is not found for this resource"
                )
            doc["methods"][method] = MethodDoc(method).to_dict(self)


class MethodDoc(object):
    """
    This class holds details about a method.

    Args:
        method: (str) : The method name
        input: (str) : Optional input if necessary, otherwise default
        input_modifier: (str) : Optional input of process_{method}_inputs
        before_commit: (str) : Optional before_commit description
        after_commit: (str) : Optional after_commit description
        use_default_response: (bool) : A flag to overwrite responses
        responses: (list) : A list of possible custom responses

    """

    def __init__(
        self,
        method,
        input=None,
        input_modifier=None,
        before_commit=None,
        after_commit=None,
        use_default_response=True,
        responses=None,
    ):
        self.method = method
        self.input = input
        self.input_modifier = input_modifier
        self.before_commit = before_commit
        self.after_commit = after_commit
        self.use_default_response = True

        if responses is None:
            self.responses = []
        else:
            self.responses = responses

    def _get_inputs(self, resource_class):
        """Dispatch to the right input type."""
        if self.method in ["get", "delete"]:
            input_dict = self._get_input_keys(resource_class)
        else:
            input_dict = self._get_input_props(resource_class)

        return input_dict

    @staticmethod
    def _get_input_keys(resource_class):
        "Extract keys for methods"
        db = resource_class.model_class.db
        keys = resource_class.get_key_names()
        if len(keys) > 1:
            return [
                dict([[key, db.doc_column(resource_class.model_class, key)]])
                for key in keys
            ]
        else:
            key = keys[0]
            return {key: db.doc_column(resource_class.model_class, key)}

    @staticmethod
    def _get_input_props(resource_class):

        return resource_class.model_class.filter_columns(
            column_props=["!readOnly"], to_camel_case=True,
        )

    @staticmethod
    def _get_url(doc, method, resource_class):
        if method in ["get", "put", "patch", "delete"]:
            if resource_class.is_collection():
                doc["url"] = resource_class.get_urls()[0]
            else:
                doc["url"] = resource_class.get_urls()[1]
        else:
            doc["url"] = resource_class.get_urls()[0]

    def to_dict(self, meta_doc):
        """Convert attributes to a dictionary"""
        resource_class = meta_doc.resource_class
        model_class = resource_class.model_class
        db = model_class.db
        doc = {}
        self._get_url(doc, self.method, resource_class)

        doc["requirements"] = self.get_method_decorators(meta_doc)
        if meta_doc.resource_class.is_collection():
            doc["queryString"] = self._get_inputs(resource_class)

            # hard-coded for the moment
            doc["jobParams"] = {
                "orderBy": {"type": "string", "list": True},
                "maxPageSize": {"type": "integer"},
                "offset": {"type": "integer"},
                "debug": {"type": "boolean"},
            }
        else:
            doc["input"] = self._get_inputs(resource_class)

        if self.input_modifier is not None:
            doc["input_modifier"] = self.input_modifier
        if self.before_commit is not None:
            doc["before_commit"] = self.before_commit
        if self.after_commit is not None:
            doc["after_commit"] = self.after_commit

        if self.responses:
            doc["responses"] = self.responses

        elif self.use_default_response:
            doc["responses"] = [self.get_default_response(meta_doc)]

        return doc

    def get_method_decorators(self, meta_doc):
        """
        This function returns a string representation of any method
        decorators.

        Args:
            meta_doc: (obj) : The meta document being processed.

        Returns:
            (list : None) : The string list of method decorator names.
        """
        method_decorators = meta_doc.resource_class.method_decorators
        if isinstance(method_decorators, list):
            return [item.__name__ for item in method_decorators]

        if isinstance(method_decorators, dict):
            if self.method in method_decorators:
                return [
                    item.__name__ for item in method_decorators[self.method]
                ]

        return None

    def get_default_response(self, meta_doc):
        """
        This function returns the standard response for the method. If something
        special is done, then the default response would be supressed.
        """
        resource = meta_doc.resource_class
        method = self.method
        db = resource.model_class.db

        outputs = {}
        if method != "delete":

            serial_fields = resource._get_serial_fields(
                method, with_class=True
            )

            if isinstance(serial_fields, dict):
                # foreign class
                foreign_class, serial_fields = list(serial_fields.items())[0]
                # NOTE: serial field relations is unresolved
                doc = db.doc_table(
                    foreign_class,
                    serial_fields=serial_fields,
                    serial_field_relations=resource._get_serial_field_relations(
                        method
                    ),
                    to_camel_case=True,
                )[foreign_class._class()]
            else:
                if serial_fields is None:
                    serial_fields = resource.model_class.get_serial_fields()

                doc = db.doc_table(
                    resource.model_class,
                    serial_fields=serial_fields,
                    serial_field_relations=resource._get_serial_field_relations(
                        method
                    ),
                    to_camel_case=True,
                )[resource.model_class._class()]

            outputs["fields"] = doc["properties"]
            # NOTE: here is where the default sort would go for collections

        return outputs
