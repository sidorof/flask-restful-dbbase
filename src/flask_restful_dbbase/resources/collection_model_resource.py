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
from ..validations import validate_process


class CollectionModelResource(DBBaseResource):
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
    process_get_input = None
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

    # def _page_configs(self, configs):
    #     """
    #     Converts any config variables to snake case and
    #     verifies the variables are part of page configs.
    #
    #     NOTE: what if a None or null is sent through?
    #     """
    #     tmp = {}
    #     if isinstance(configs, list):
    #         configs = configs[0]
    #
    #     if isinstance(configs, str):
    #         configs = json.loads(configs.replace("'", '"'))
    #
    #     for key, value in configs.items():
    #         new_key = xlate(key, camel_case=False)
    #         if new_key in self._PAGE_CONFIGS:
    #             # run the gauntlet
    #             if new_key == "order_by":
    #                 # account for field name conversion
    #                 if isinstance(value, list):
    #                     new_value = [
    #                         xlate(val, camel_case=False) for val in value
    #                     ]
    #                 else:
    #                     new_value = [xlate(value, camel_case=False)]
    #
    #             elif new_key == "limit":
    #                 new_value = int(value)
    #
    #             elif new_key == "page_size":
    #                 new_value = int(value)
    #                 if self.max_page_size is not None:
    #                     new_value = min(new_value, self.max_page_size)
    #
    #             elif new_key in ["page_size", "offset", "limit"]:
    #                 new_value = int(value)
    #
    #             elif new_key == "debug":
    #                 new_value = value.lower() == "true"
    #             else:
    #                 # new_key == "serial_fields"
    #                 new_value = [xlate(val, camel_case=False) for val in value]
    #
    #             tmp[new_key] = new_value
    #
    #         else:
    #             raise ValueError(f"Unknown page config value: {new_key}")
    #
    #     if "order_by" not in tmp and self.order_by is not None:
    #         if isinstance(self.order_by, list):
    #             tmp["order_by"] = self.order_by
    #         else:
    #             tmp["order_by"] = [self.order_by]
    #
    #     return tmp

    # def _filter_var(self, value):
    #     """
    #     Creates comparison variable from "var:variable"
    #     """
    #     comp_var = xlate(value[4:], camel_case=False)
    #     return getattr(self.model_class, comp_var)
    #
    # def _filter_op1(self, op, var, value):
    #     """
    #     Creates column variable and filter for op1 operators"
    #     """
    #     col_var = getattr(
    #         self.model_class,
    #         xlate(var, camel_case=False)
    #     )
    #
    #     if value.startswith("var:"):
    #         value = self._filter_var(value)
    #     func = getattr(col_var, f"__{op}__")
    #     return func(value)
    #
    # def _filter_op2(self, op, var, value):
    #     """
    #     Creates column variable and filter for op2 operators"
    #     """
    #     col_var = getattr(
    #         self.model_class,
    #         xlate(var, camel_case=False)
    #     )
    #     func = getattr(col_var, op)
    #     return func(value)
    #
    # def _filter_in(self, var, value):
    #     """
    #     Creates a column variable and filter for in list.
    #     """
    #     if isinstance(value, list):
    #         col_var = getattr(self.model_class, var)
    #         return column.in_(value)
    #
    #     msg = f"Value must be a list: {value}"
    #     current_app.logger.info(msg)
    #     raise ValueError(msg)
    #
    # def _filter(self, item):
    #     """
    #     Structure of item:
    #         {"var": var, "filter": {"op": op, "value": value}}
    #     """
    #     var, op, value = self._parse_filter(item)
    #
    #     col_var = xlate(var, camel_case=False)
    #     if op == "in":
    #         clause = self._filter_in(col_var, value)
    #     elif op in self.OP_CODES1:
    #         clause = self._filter_op1(op, col_var, value)
    #     elif op in self.OP_CODES2:
    #         clause = self._filter_op2(op, col_var, value)
    #     else:
    #         msg = f"unknown op code: {op}"
    #         current_app.logger.info(msg)
    #         raise ValueError(msg)
    #     return clause
    #
    # def _parse_filter(self, item):
    #     if not isinstance(item, dict):
    #         msg = f"Item must be a dict: {item}"
    #         current_app.logger.info(msg)
    #         raise ValueError(msg)
    #
    #     if "var" not in item:
    #         msg = f"a column variable is required {item}"
    #         current_app.logger.info(msg)
    #         raise ValueError(msg)
    #
    #     if "filter" not in item:
    #         msg = f"a filter is required {item}"
    #         current_app.logger.info(msg)
    #         raise ValueError(msg)
    #
    #     filter_ = item["filter"]
    #
    #     if "op" not in filter_:
    #         msg = f"an 'or' is required {filter_}"
    #         current_app.logger.info(msg)
    #         raise ValueError(msg)
    #
    #     if "value" not in filter_:
    #         msg = f"a 'value' is required {filter_}"
    #         current_app.logger.info(msg)
    #         raise ValueError(msg)
    #
    #     var = item["var"]
    #     op = filter_["op"]
    #     value = filter_["value"]
    #
    #     return var, op, value
    #
    # def _classify_op(self, var, value):
    #     """
    #     Classifies the operation using the variable. Also,
    #     translation from camel to snake takes place as well
    #
    #     var, value
    #         select where var = value   normal
    #
    #     var[], list | single value
    #         select item1 or item2 or item3 ...
    #
    #     value, (op, value)
    #         "eq ne gt lt ..."
    #
    #     return
    #         op, new_var, value
    #
    #     """
    #     if var.endswith("[]"):
    #         new_var = xlate(var[:-2], camel_case=False)
    #         return new_var, "in", value
    #
    #     try:
    #         value = json.loads(value[0])
    #     except:
    #         pass
    #
    #     if isinstance(value, dict) and len(value) == 2:
    #         # Note that val could be a variable such as var:my_variable
    #         # xlate of my_variable is handled when adding to query filter
    #         op, val = value.values()
    #         new_var = xlate(var, camel_case=False)
    #
    #         if op not in self.OP_CODES1 + self.OP_CODES2:
    #             str_list = str(self.OP_CODES1 + self.OP_CODES2).replace(
    #                 "'", ""
    #             )
    #             raise ValueError(
    #                 f'Op code "{op}" wrong. Must be in {str_list}'
    #             )
    #
    #         return new_var, op, val
    #
    #     if isinstance(value, list) and len(value) == 1:
    #         if value[0] in self.OP_CODES1 + self.OP_CODES2:
    #             # mistake concluded
    #             raise ValueError(
    #                 "There must be a value paired with the operator. "
    #                 "Example: [operator, value]"
    #             )
    #         if value in [["None"], ["null"]]:
    #             value = None
    #         new_var = xlate(var, camel_case=False)
    #
    #         return new_var, "eq", value
    #
    #     # default
    #     new_var = xlate(var, camel_case=False)
    #
    #     return new_var, "eq", value
    #
    # def process_filters(self, filters, query):
    #     """
    #     NOTE: this is an early pass at POST queries. It needs
    #         enriching on features and design. Also, it needs
    #         integration with features in common with GET.
    #     For processing in POST
    #     Separate dictionary for each item to enable
    #     dupe fields
    #
    #     format = [
    #         { field: { op: operator, value: val}}
    #         { field: { op: operator, value: val}}
    #         { field: { op: operator, value: val}}
    #     ]
    #
    #     example: {
    #         var: description,
    #         filter: {
    #             op: 'ilike',    operator
    #             value: 'val1'   value
    #         }
    #     }
    #
    #     for each filter, look first for an op,
    #         if yes, it's probably an 'or'
    #         if no, process as variable
    #     params = {
    #         "query": {
    #             "filters": [
    #                 {
    #                     "op": "or",
    #                     "value": [
    #                         {
    #                             "description": {
    #                                 "op":"ilike",
    #                                 "value":"%coin%"
    #                             }
    #                         },
    #                         {
    #                             "description": {
    #                                 "op": "ilike",
    #                                 "value": "%sterling%"
    #                             }
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     }
    #
    #     """
    #     for item in filters:
    #         # item {'description': '{"op":"ilike","value":"%coin%"}'}
    #         if "op" in item:
    #             # is it a field or and/or
    #             #   (skipping 'and' for now)
    #             #   also, see how this only does one level of 'or'
    #             op = item["op"]
    #             if op == "or":
    #                 # should be 2+ clauses
    #                 value = item["value"]
    #                 length = len(value)
    #                 if length == 1:
    #                     msg = "Cannot have an 'or' with one clause"
    #                     current_app.logger.info(msg)
    #                     raise ValueError(msg)
    #
    #                 if length >= 2:
    #                     col_filter0 = self._filter(value[0])
    #                     col_filter1 = self._filter(value[1])
    #
    #                     clause_list = col_filter0 | col_filter1
    #
    #                     for i in range(2, len(value)):
    #                         clause_list.append(self._filter(value[i]))
    #
    #                     query = query.filter(clause_list)
    #
    #             else:
    #                 msg = f"op of {op} is not supported"
    #                 current_app.logger.info(msg)
    #                 raise ValueError(msg)
    #         else:
    #             query = query.filter(self._filter(item))
    #
    #     return query

    def get(self, **kwargs):
        """ Get method"""
        FUNC_NAME = "GET"
        name = self.model_class._class()
        url = request.path
        current_app.logger.info(f"{FUNC_NAME} {url} {kwargs}")

        data = request.args.to_dict(flat=False)
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

        query = self.model_class.query

        if self.process_get_input is not None:
            # single values will still be in a list at this point
            # Ex: {id: [40]}"

            # format for output:
            #   To continue processing after updates or changes:
            #       {"status": True, "query", query, "data": data}
            #   To exit the scene:
            #       {
            #           "status": False,
            #           "message", msg,
            #           "status_code": status_code
            #       }
            #   Anything other than that results in a 500 error
            current_app.logger.debug("  Starting process_get_input function")
            try:
                output = self.process_get_input(query, data)
            except Exception as err:
                current_app.logger.error(err.args)
                return "Failure in process_get_input function", 500

            current_app.logger.debug("  Completed process_get_input function")
            # bare minimum check
            validate_process(output, true_keys=["query", "data"])
            current_app.logger.debug("  Completed validate_process function")

            if output["status"]:
                current_app.logger.debug(
                    "  Output process_get_input status: True"
                )
                query = output["query"]
                data = output["data"]
            else:
                message = output["message"]
                status_code = output["status_code"]

                current_app.logger.debug(
                    "  Output process_get_input status: False"
                )
                current_app.logger.debug(
                    f"  Message: {message}, {status_code}"
                )
                return {"message": message}, status_code

        query_data = []

        current_app.logger.debug("  Converting query parameters")
        for var, value in data.items():
            # classify op and convert var from camel_case
            try:
                query_data.append(self._classify_op(var, value))
            except Exception as err:
                return {"message": f"{err.args}"}, 400
        current_app.logger.debug("  Completed conversion")

        obj_params = self.get_obj_params()
        query_data = [
            [var, op, value]
            for var, op, value in query_data
            if var in obj_params
        ]

        # query filtering
        current_app.logger.debug("  Building SqlAlchemy query filtering")
        for new_var, op, value in query_data:
            var = getattr(self.model_class, new_var)
            if isinstance(value, str) and value[:4] == "var:":
                # also a variable
                comp_var = xlate(value[4:], camel_case=False)
                value = getattr(self.model_class, comp_var)

            if isinstance(value, list):
                query = query.filter(var.in_(value))

            elif op in self.OP_CODES1:
                func = getattr(var, f"__{op}__")
                query = query.filter(func(value))

            else:
                # bad op codes already weeded out above
                func = getattr(var, op)
                query = query.filter(func(value))

        current_app.logger.debug("  Adding order_by to SqlAlchemy query")
        if order_by:
            msg = "{order} is not a column in {name}"
            order_list = []
            for order in order_by:
                if order.startswith("-"):
                    order = order[1:]
                    if hasattr(self.model_class, order):
                        order_list.append(
                            getattr(self.model_class, order).desc()
                        )
                    else:
                        return (
                            {"message": msg.format(order=order, name=name)},
                            400,
                        )
                else:
                    if hasattr(self.model_class, order):
                        order_list.append(getattr(self.model_class, order))
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
            if self.process_get_input is None:
                get_input_doc = None
            else:
                get_input_doc = inspect.getdoc(self.process_get_input)
            return {
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
                "query": str(query),
            }, 200

        current_app.logger.debug("  Completed SqlAlchemy query:")
        current_app.logger.debug(f"  {query}")
        query = query.all()

        if serial_fields is None:
            serial_fields, serial_field_relations = self._get_serializations(
                "get"
            )

        try:
            current_app.logger.debug("  Returning completed query")
            return (
                {
                    self.model_class._class(): [
                        item.to_dict(
                            serial_fields=serial_fields,
                            serial_field_relations=serial_field_relations,
                        )
                        for item in query
                    ],
                },
                200,
            )

        except Exception as err:
            msg = err.args[0]
            return_msg = f"Internal Server Error: method {FUNC_NAME}: {url}"
            current_app.logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 500
