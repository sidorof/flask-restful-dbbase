# flask_restful/resources/collection_model_resource.py
""""
This module implements a starting point for collection model resources.

"""
import json
import inspect

from dbbase.utils import xlate
from flask import current_app
from flask_restful import request
from .dbbase_resource import DBBaseResource

from ..queries import process_filters
from ..queries import page_configs
from ..queries import process_filters

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

    _PAGE_CONFIGS = [
        "page_size",
        "offset",
        "limit",
        "debug",
        "order_by",
        "serial_fields",
    ]

    # codes instantiated as field.__op__
    OP_CODES1 = ["eq", "ne", "gt", "ge", "lt", "le"]

    # codes instantiated as:
    #   func = getattr(column.field, "ilike")
    #   filter(func(value))
    OP_CODES2 = ["contains", "like", "ilike", "notlike", "notilike"]

    def __init__(self):
        # super().__init__()
        DBBaseResource.__init__(self)
        if self.model_class is None:
            msg = "A model class must be set for this resource to function."
            raise ValueError(msg)
        self.model_name = self.model_class._class()

    def post(self, **kwargs):
        """ Post method"""
        FUNC_NAME = "POST"
        name = self.model_class._class()
        url = request.path
        status_code = 200

        current_app.logger.info(f"{FUNC_NAME} {url} {kwargs}")

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

        orig_data = request.args.to_dict(flat=False)

        configs = {}
        for key in ["pageConfig", "page_config"]:
            if key in data:
                configs = self._page_configs(data.pop(key))
                break

        order_by = configs.get("order_by")
        page_size = configs.get("page_size")
        limit = configs.get("limit")
        offset = configs.get("offset")
        serial_fields = configs.get("serial_fields")
        serial_field_relations = configs.get("serial_field_relations")
        debug = configs["debug"] if "debug" in configs else False

        current_app.logger.debug(f"  order_by: {order_by}")
        current_app.logger.debug(f"  page_size: {page_size}")
        current_app.logger.debug(f"  limit: {limit}")
        current_app.logger.debug(f"  offset: {offset}")
        current_app.logger.debug(f"  serial_fields: {serial_fields}")
        current_app.logger.debug(
            f"  serial_field_relations: {serial_field_relations}"
        )
        current_app.logger.debug(f"  debug: {debug}")
        # end of page config

        query = res.model_class.query

        filters = data["query"].get("filters", None)

        if filters:
            query = process_filters(res, filters, query)

        current_app.logger.debug("  Adding order_by to SqlAlchemy query")
        if order_by:
            msg = "{order} is not a column in {name}"
            order_list = []
            for order in order_by:
                if order.startswith("-"):
                    order = order[1:]
                    if hasattr(res.model_class, order):
                        order_list.append(
                            getattr(res.model_class, order).desc()
                        )
                    else:
                        return (
                            {"message": msg.format(order=order, name=name)},
                            400,
                        )
                else:
                    if hasattr(res.model_class, order):
                        order_list.append(getattr(res.model_class, order))
                    else:
                        return (
                            {"message": msg.format(order=order, name=name)},
                            400,
                        )

            query = query.order_by(*order_list)

        if offset is not None:
            current_app.logger.debug("  Adding offset to SqlAlchemy query")
            query = query.offset(offset)

        if page_size is not None:
            current_app.logger.debug("  Adding page_size to SqlAlchemy query")
            query = query.limit(page_size)

        if limit is not None:
            current_app.logger.debug("  Adding limit to SqlAlchemy query")
            # works same as page size, more familiar for dbs
            query = query.limit(limit)

        if debug:
            current_app.logger.debug("  Building debug explanation")
            if res.process_post_input is None:
                post_input_doc = None
            else:
                post_input_doc = inspect.getdoc(res.process_post_input)
            return {
                "class_defaults": {
                    "model_name": res.model_name,
                    "process_post_input": post_input_doc,
                    "max_page_size": res.max_page_size,
                    "order_by": None,
                    "op_codes": OP_CODES1 + OP_CODES2,
                },
                # "original_data": orig_data,
                "converted_data": data,
                "page_configs": configs,
                "query": str(query),
            }, 200

        current_app.logger.debug("  Completed SqlAlchemy query:")
        current_app.logger.debug(f"  {query}")
        query = query.all()

        if serial_fields is None:
            serial_fields, serial_field_relations = res._get_serializations(
                "get"
            )

        try:
            current_app.logger.debug("  Returning completed query")

            answer = {
                    res.model_class._class(): [
                        item.to_dict(
                            serial_fields=serial_fields,
                            serial_field_relations=serial_field_relations,
                        )
                        for item in query
                    ],
                }
            current_app.logger.debug(f"Returning {answer}")

            return (
                {
                    res.model_class._class(): [
                        item.to_dict(
                            serial_fields=serial_fields,
                            serial_field_relations=serial_field_relations,
                        )
                        for item in query
                    ],
                },
                200,
                {
                    'Content-type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            )

        except Exception as err:
            msg = err.args[0]
            status_code = 500
            return_msg = f"Internal Server Error: method {FUNC_NAME}: {url}"
            current_app.logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 500

        return {
            "status": False,
            "message": message,
            "status_code": status_code
        }
