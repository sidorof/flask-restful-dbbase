# flask_restful/resources/collection_model_resource.py
""""
This module implements a starting point for collection model resources.

"""
from sqlalchemy.exc import IntegrityError
from flask_restful import request
from .dbbase_resource import DBBaseResource
#from . import db


class CollectionModelResource(DBBaseResource):
    """
    CollectionModelResource Class

    This model class implements the base class.

    model_class: a dbbase.Model
    url_prefix: the portion of the path leading up to the resource
        For example: /api/v2

    url_path: the url_path defaults to a lower case version of the
        the model_class name if left as None, but can have an
        explicit name if necessary.

    serial_fields: if left as None, it uses the serial list from
        the model class. However, it can be a list of field names
        or

    max_page_size = None

    """
    @classmethod
    def get_urls(cls):
        """get_urls

        This version the function returns just the base url, unlike
        the ModelResource.

        """
        if cls.model_class is None:
            raise ValueError('A model class must be defined')

        return [cls.create_url()]

    def get(self, **kwargs):
        name = self.model_class._class()
        import json
        print('kwargs', kwargs)
        #input('ready')

        # query goes here
        # print(dir(request))
        print('request.base_url', request.base_url)
        print('request.content_type', request.content_type)
        print('request.query_string', request.query_string)
        print('request.values', request.values)
        print('request.args', request.args)
        #print('request.json', request.json)
        print('-------------------------------------------')
        #a = request.get_json(force=True)
        obj_params = self.get_obj_params()
        print('i am here')

        query = request.values.get('query')
        print('query', query)
        #print(str(args), args)

        input('ready')

        if query is not None:
            print('this goes to subsystem for queries')
            print('request.values for query', request.values)
            print()
            qry = []
            query = request.values['query']
            for key, value in query.items():
                print('key', key)
                print('value', value)


            input('ready')
            return qry
        else:
            print('this is handled by straight key values')
            qry = self.model_class.query
            if request.args:
                query_data = self.model_class.deserialize(request.args)
                print('query_data', query_data)
            print(qry)
            qry = qry.all()

        sfields, sfield_relations = self._get_serializations("post")

        return ([
            item.to_dict(
                serial_fields=sfields,
                serial_field_relations=sfield_relations,
            ) for item in qry],
            200,
        )
