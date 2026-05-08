# queries.py
from flask import current_app

PAGE_CONFIGS = [
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


def query(res, data):
    """
    Implements a complex query within a POST.

    It is meant to be used as follows:

    process_post_input = query

    This looks for a key of 'query' in the data, if found
    the query is processed.
    """
    # enforce it is a query
    if "query" not in data:
        return_msg = "Missing the 'query' key."
        current_app.logger.error(return_msg)
        return {"message": return_msg}, 400

    # NOTE: dupe code alert
    # page configs
    configs = {}
    for key in ["pageConfig", "page_config"]:
        if key in data:
            configs = page_configs(data.pop(key))
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

def _filter_var(res, value):
    """
    Creates comparison variable from "var:variable"
    """
    comp_var = xlate(value[4:], camel_case=False)
    return getattr(res.model_class, comp_var)

def _filter_op1(res, op, var, value):
    """
    Creates column variable and filter for op1 operators"
    """
    col_var = getattr(
        res.model_class,
        xlate(var, camel_case=False)
    )

    if value.startswith("var:"):
        value = res._filter_var(value)
    func = getattr(col_var, f"__{op}__")
    return func(value)

def _filter_op2(res, op, var, value):
    """
    Creates column variable and filter for op2 operators"
    """
    col_var = getattr(
        res.model_class,
        xlate(var, camel_case=False)
    )
    func = getattr(col_var, op)
    return func(value)

def _filter_in(res, var, value):
    """
    Creates a column variable and filter for in list.
    """
    if isinstance(value, list):
        col_var = getattr(res.model_class, var)
        return column.in_(value)

    msg = f"Value must be a list: {value}"
    current_app.logger.info(msg)
    raise ValueError(msg)

def _filter(res, item):
    """
    Structure of item:
        {"var": var, "filter": {"op": op, "value": value}}
    """
    var, op, value = res._parse_filter(item)

    col_var = xlate(var, camel_case=False)
    if op == "in":
        clause = res._filter_in(col_var, value)
    elif op in OP_CODES1:
        clause = res._filter_op1(op, col_var, value)
    elif op in OP_CODES2:
        clause = res._filter_op2(op, col_var, value)
    else:
        msg = f"unknown op code: {op}"
        current_app.logger.info(msg)
        raise ValueError(msg)
    return clause

def _parse_filter(res, item):
    if not isinstance(item, dict):
        msg = f"Item must be a dict: {item}"
        current_app.logger.info(msg)
        raise ValueError(msg)

    if "var" not in item:
        msg = f"a column variable is required {item}"
        current_app.logger.info(msg)
        raise ValueError(msg)

    if "filter" not in item:
        msg = f"a filter is required {item}"
        current_app.logger.info(msg)
        raise ValueError(msg)

    filter_ = item["filter"]

    if "op" not in filter_:
        msg = f"an 'or' is required {filter_}"
        current_app.logger.info(msg)
        raise ValueError(msg)

    if "value" not in filter_:
        msg = f"a 'value' is required {filter_}"
        current_app.logger.info(msg)
        raise ValueError(msg)

    var = item["var"]
    op = filter_["op"]
    value = filter_["value"]

    return var, op, value

def _classify_op(res, var, value):
    """
    Classifies the operation using the variable. Also,
    translation from camel to snake takes place as well

    var, value
        select where var = value   normal

    var[], list | single value
        select item1 or item2 or item3 ...

    value, (op, value)
        "eq ne gt lt ..."

    return
        op, new_var, value

    """
    if var.endswith("[]"):
        new_var = xlate(var[:-2], camel_case=False)
        return new_var, "in", value

    try:
        value = json.loads(value[0])
    except:
        pass

    if isinstance(value, dict) and len(value) == 2:
        # Note that val could be a variable such as var:my_variable
        # xlate of my_variable is handled when adding to query filter
        op, val = value.values()
        new_var = xlate(var, camel_case=False)

        if op not in OP_CODES1 + OP_CODES2:
            str_list = str(OP_CODES1 + OP_CODES2).replace(
                "'", ""
            )
            raise ValueError(
                f'Op code "{op}" wrong. Must be in {str_list}'
            )

        return new_var, op, val

    if isinstance(value, list) and len(value) == 1:
        if value[0] in OP_CODES1 + OP_CODES2:
            # mistake concluded
            raise ValueError(
                "There must be a value paired with the operator. "
                "Example: [operator, value]"
            )
        if value in [["None"], ["null"]]:
            value = None
        new_var = xlate(var, camel_case=False)

        return new_var, "eq", value

    # default
    new_var = xlate(var, camel_case=False)

    return new_var, "eq", value

def process_filters(res, filters, query):
    """
    NOTE: this is an early pass at POST queries. It needs
        enriching on features and design. Also, it needs
        integration with features in common with GET.
    For processing in POST
    Separate dictionary for each item to enable
    dupe fields

    format = [
        { field: { op: operator, value: val}}
        { field: { op: operator, value: val}}
        { field: { op: operator, value: val}}
    ]

    example: {
        var: description,
        filter: {
            op: 'ilike',    operator
            value: 'val1'   value
        }
    }

    for each filter, look first for an op,
        if yes, it's probably an 'or'
        if no, process as variable
    params = {
        "query": {
            "filters": [
                {
                    "op": "or",
                    "value": [
                        {
                            "description": {
                                "op":"ilike",
                                "value":"%coin%"
                            }
                        },
                        {
                            "description": {
                                "op": "ilike",
                                "value": "%sterling%"
                            }
                        }
                    ]
                }
            ]
        }
    }

    """
    for item in filters:
        # item {'description': '{"op":"ilike","value":"%coin%"}'}
        if "op" in item:
            # is it a field or and/or
            #   (skipping 'and' for now)
            #   also, see how this only does one level of 'or'
            op = item["op"]
            if op == "or":
                # should be 2+ clauses
                value = item["value"]
                length = len(value)
                if length == 1:
                    msg = "Cannot have an 'or' with one clause"
                    current_app.logger.info(msg)
                    raise ValueError(msg)

                if length >= 2:
                    col_filter0 = _filter(res, value[0])
                    col_filter1 = _filter(res, value[1])

                    clause_list = col_filter0 | col_filter1

                    for i in range(2, len(value)):
                        clause_list.append(_filter(res, value[i]))

                    query = query.filter(clause_list)

            else:
                msg = f"op of {op} is not supported"
                current_app.logger.info(msg)
                raise ValueError(msg)
        else:
            query = query.filter(res._filter(item))

    return query
