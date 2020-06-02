# flask_restful/resources/model_resource.py
""""
This module implements a starting point for model resources.

"""
from sqlalchemy.exc import IntegrityError
from flask_restful import request
from .dbbase_resource import DBBaseResource
#from . import db


class ModelResource(DBBaseResource):
    """
    ModelResource Class

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

    """

    def get(self, **kwargs):
        print('i am here')
        name = self.model_class._class()
        print('kwargs', kwargs)
        print('query_string', request.query_string)
        key_name, key = self._check_key(kwargs)
        print('key_name', key_name)
        print('key', key)
        if key is None:
            return {"message": f"No key for {name} given"}, 404
        item = self.model_class.query.get(key)

        print(item, item)

        serial_fields, serial_field_relations = self._get_serializations(
            "get"
        )

        if item:
            return (
                item.to_dict(
                    serial_fields=serial_fields,
                    serial_field_relations=serial_field_relations,
                ),
                200
            )

        return (
            {
                "error": {
                    "message": f"{name} with {key_name} of {key} not found",
                }
            },
            404
        )

    def post(self):
        """ Post """
        print('you have reached a single post')
        
        status, data = self.screen_data(
            self.model_class.deserialize(request.get_json()),
            self.get_obj_params()
        )

        key_name = self.get_key(formatted=False)
        name = self.model_class._class()

        if key_name in data:
            item = self.model_class.query.get(data[key_name])

            if item:
                return {"message": f"{key} for {name} already exists."}, 409

        item = self.model_class(**data)

        # if foreign_key, trip #2 to the db
        status, errors = item.validate_record(camel_case=True)

        item = self.pre_save(item)

        try:
            # NOTE: consider possibility to just let it trainwreck once
            # #3 trip to the db
            item.save()
        except IntegrityError as err:
            # may be helpful
            msg = str(err).split("\n")[0]
            self.model_class.db.session.rollback()
            return {"message": msg}, 400

        except Exception as err:
            name = self.model_class._class()
            self.model_class.db.session.rollback()
            return (
                {"message": f"An error occurred inserting the {name}."},
                500,
            )

        item = self.post_save(item)

        ser_list, rel_ser_lists = self._get_serializations("post")

        return (
            item.to_dict(
                serial_fields=ser_list,
                serial_field_relations=rel_ser_lists,
            ),
            201,
        )

    def put(self, **kwargs):
        """ Put """

        key_name, key = self._check_key(kwargs)
        name = self.model_class._class()

        status, data = self.screen_data(
            self.model_class.deserialize(request.get_json()),
            self.get_obj_params()
        )

        if status:
            if key_name in data:
                if data[key_name] != key:
                    msg = f"{key_name} for {name} must match "
                    f"the url key:{key}"
                return {"message": msg}, 400

            item = self.model_class.query.get(key)
           
            # if foreign_key, trip #2 to the db
            status, errors = item.validate_record(camel_case=True)

            item = self.pre_save(item)

            try:
                # NOTE: consider possibility to just let it trainwreck once
                # #3 trip to the db
                item.save()
            except IntegrityError as err:
                # may be helpful
                msg = str(err).split("\n")[0]
                db.session.rollback()
                return {"message": msg}, 400

            except Exception as err:
                name = self.model_class._class()
                db.session.rollback()
                return (
                    {"message": f"An error occurred inserting the {name}."},
                    500,
                )

            ser_list, rel_ser_lists = self._get_serializations("put")

            item = self.post_save(item)

            return (
                item.to_dict(
                    serial_fields=ser_list,
                    serial_field_relations=rel_ser_lists,
                ),
                202,
            )

        return data, 400

    def patch(self, **kwargs):
        """ Patch

        """
        key_name, key = self._check_key(kwargs)
        name = self.model_class._class()

        status, data = self.screen_data(
            self.model_class.deserialize(request.get_json()),
            self.get_obj_params(), skip_missing_data=True
        )

        if status is False:
            return {"message": data}, 400

        if key_name in data:
            if data[key_name] != key:
                msg = f"{key_name} for {name} must match the url key: {key}"
                return {"message": msg}, 400

        item = self.model_class.query.get(key)

        if item:
            for key, value in data.items:
                setattr(item, key, value)

            item = self.pre_save(item)
            item.save()
            item = self.post_save(item)

            ser_list, rel_ser_lists = self._get_serializations("patch")

            return (
                item.to_dict(
                    serial_fields=ser_list,
                    serial_field_relations=rel_ser_lists,
                ),
                202,
            )
        return {'message': 'Item not found.'}, 404

    def delete(self, **kwargs):
        """ Delete
        """
        key_name, key = self._check_key(kwargs)
        name = self.model_class._class()

        item = self.model_class.query.get(key)

        if item:
            try:
                item.delete()
                return {"message": f"{name} deleted"}

            except IntegrityError as err:
                # may be helpful
                msg = str(err).split("\n")[0]
                self.model_class.dbsession.rollback()
                return {"message": msg}, 400

            except Exception as err:
                self.model_class.dbsession.rollback()
                return (
                    {"message": f"An error occurred inserting the {name}."},
                    500,
                )

        return {'message': f'{name} not found.'}, 404
