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

    process_get_input = None
    order_by = None
    max_page_size = None

    @classmethod
    def get_urls(cls):
        """get_urls

        This version the function returns just the base url, unlike
        the ModelResource.

        """
        if cls.model_class is None:
            raise ValueError("A model class must be defined")

        return [cls.create_url()]

    def get(self):

        name = self.model_class._class()
        url = request.path
        if request.values:
            data = request.values
        elif request.data:
            data = request.data
        elif request.query_string:
            data = request.query_string
        else:
            data = request.args

        query = self.model_class.query

        if self.process_get_input is not None:
            query = self.process_get_input(query, data)

        data = self.model_class.deserialize(data)
        # extract job params first -- filtered out below
        order_by = data.get("order_by", self.order_by)
        page_size = data.get("page_size", None)
        offset = data.get("offset", None)
        page = data.get("page", None)
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
            if isinstance(order_by, list):
                for order in order_by:
                    order = xlate(order, camel_case=False)
                    query = query.order_by(getattr(self.model_class, order))
            else:
                query = query.order_by(getattr(self.model_class, order_by))

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
