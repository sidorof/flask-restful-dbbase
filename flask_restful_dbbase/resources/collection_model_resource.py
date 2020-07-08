# flask_restful/resources/collection_model_resource.py
""""
This module implements a starting point for collection model resources.

"""
from dbbase.utils import xlate
from flask_restful import request
from .dbbase_resource import DBBaseResource
import logging

logger = logging.getLogger(__file__)


class CollectionModelResource(DBBaseResource):
    """
    CollectionModelResource Class

    This model class implements the base class.

    """

    model_name = None
    process_get_input = None
    max_page_size = None
    order_by = None

    def __init__(self):
        if self.model_class is None:
            msg = "A model class must be set for this resource to function."
            raise ValueError(msg)
        self.model_name = self.model_class._class()
        super().__init__()

    def get(self):

        FUNC_NAME = "get"
        name = self.model_class._class()
        url = request.path
        data = request.args

        # special - could be a list of fields
        order_by = request.args.getlist("orderBy", self.order_by)

        query = self.model_class.query
        if self.process_get_input is not None:

            status, result = self.process_get_input(query, data)
            if status is False:
                # exit the scene, data should be a
                # tuple of message and status
                if isinstance(result, tuple):
                    return result
                else:
                    func = self.process_get_input.__name__
                    msg = f"malformed error in {func}: {result}"
                    return {"message": msg}, 500
            query, data = result

        data = self.model_class.deserialize(data)
        # extract job params first -- filtered out below

        # params not data so not converted
        page_size = data.get("page_size", None)
        offset = data.get("offset", None)
        debug = data.get("debug", None)

        if debug == "False":
            debug = False

        if page_size is not None:
            if self.max_page_size is not None:
                page_size = min(int(page_size), self.max_page_size)

        # for later
        # qquery = request.values.get('query', None)

        query_data = self.model_class.deserialize(data)

        obj_params = self.get_obj_params()

        query_data = dict(
            [
                [key, value]
                for key, value in query_data.items()
                if key in obj_params
            ]
        )

        for key, value in query_data.items():
            query = query.filter(getattr(self.model_class, key) == value)

        if order_by:
            msg = "{order} is not a column in {name}"
            order_list = []
            for order in order_by:
                order = xlate(order, camel_case=False)
                if hasattr(self.model_class, order):
                    order_list.append(getattr(self.model_class, order))
                else:
                    return (
                        {"message": msg.format(order=order, name=name)},
                        400,
                    )
            query = query.order_by(*order_list)

        if offset is not None:
            query = query.offset(offset)

        if page_size is not None:
            if offset is not None:
                query = query.limit(page_size)
            else:
                query = query.limit(page_size)
        if debug:
            return {"query": str(query)}, 200

        query = query.all()
        sfields, sfield_relations = self._get_serializations("get")

        try:
            return (
                {
                    self.model_class._class(): [
                        item.to_dict(
                            serial_fields=sfields,
                            serial_field_relations=sfield_relations,
                        )
                        for item in query
                    ],
                },
                200,
            )

        except Exception as err:
            msg = err.args[0]
            return_msg = f"Internal Server Error: method {FUNC_NAME}: {url}"
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 500
