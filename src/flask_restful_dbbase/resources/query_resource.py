# flask_restful/resources/collection_model_resource.py
""""
This module implements a starting point for collection model resources.

"""
from flask import current_app
from flask_restful import request
from .dbbase_resource import DBBaseResource

from ..queries import query


class QueryResource(DBBaseResource):
    """
    CollectionModelResource Class

    This model class implements the base class.

    This class supports only gets to return collections of
    records.

    Like the ModelResource class there is a provision for a
    process_get_input function.

    The usual filtering is available for gathering records if a variable is
    a specific value. Most of the time, this will be all that is necessary.

    However, there is a means to select records by a comparison operator.

    Use a format as follows:

    query_string: {
        var1: [operator, comparison_value]
    }

    The list of operators for single comparison value is:
        ["eq", "ne", "gt", "ge", "lt", "le"]

    In addition, if comparison is made such as selecting where var1 > var2,
    use `{var1: ["gt", var:var2]}` to signal this is another variable.

    To gather records that are found in a list use var1[]: [val1, val2, ...].

    Or, for more flexibility use:

    query_string: {
        var1: [operator, [val1, val2, ...]]
    }

    The supported list of operators are
        ["like", "ilike", "notlike", "notilike"]

    To control record set sizes, a variable `page_config` is a dict of page
    or record variables.

    Bear in mind tha all variables entering can be either camel or snake based.

    Page_config variables:

        "orderBy": ["id", "statusId"],
            Can be a single value or a list
            To sort in descending order use the format -var1

        "pageSize": "50",
            The maximum page size can be limited by the class
            variable `max_page_size`

        "offset": 30,  The number of records to skip

        "limit": "100",
            limits the size of the record set

        "serialFields": ["id", "statusId"],
            can specify specific columns to be returned
            fallback: serial fields can be specified by resource or dbbase
            model

        "debug": "False",
            covered below

    if debug is true, the recordset is not returned. Instead, data returned
    consists of variables used, the default variable amounts, and the
    SqlAlchemy query that would be executed.

        "class_defaults": {
            "model_name": self.model_name,
            "process_get_input": get_input_doc,
            "max_page_size": self.max_page_size,
            "order_by": None,
            "op_codes": self.OP_CODES1 + self.OP_CODES2,
        },
        "original_data": orig_data,
        "converted_data": query_data,
        "page_configs": configs,
        "query": str(query)

    """

    model_name = None

    # not used for now
    process_post_input = None
    max_page_size = None
    order_by = None

    def __init__(self):
        # super().__init__()
        DBBaseResource.__init__(self)
        if self.model_class is None:
            msg = "A model class must be set for this resource to function."
            raise ValueError(msg)
        self.model_name = self.model_class._class()

    def post(self, **kwargs):
        """ Post method"""
        func_name = "POST"
        name = self.model_class._class()
        url = request.path
        current_app.logger.info(
            f"{name}:{func_name} {url} {kwargs}")

        if request.is_json:
            try:
                data = request.json
            except Exception as err:
                msg = err
                return_msg = f"A JSON format problem:{msg}: {request.data}"
                current_app.logger.error(return_msg)
                return {"message": return_msg}, 400

        else:
            current_app.logger.info("JSON format is required")
            return {"message": "JSON format is required"}, 415
        current_app.logger.info(f"  args received: {data}")

        return query(
            self,
            data,
            {
                "func_name": func_name,
                "name": name,
                "url": url
            }
        )
