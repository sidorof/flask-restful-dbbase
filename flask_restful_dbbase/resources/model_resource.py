# flask_restful/resources/model_resource.py
""""
This module implements a starting point for model resources.

"""
from sqlalchemy.exc import IntegrityError
from flask_restful import request
from .dbbase_resource import DBBaseResource
import logging

logger = logging.getLogger(__file__)


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
        name = self.model_class._class()

        # the correct key test - raises error if improper url
        key_name, key = self._check_key(kwargs)

        try:
            item = self.model_class.query.get(key)
        except:
            url = request.path
            msg = f"Internal Server Error: method get: {url}"
            logger.error(msg)
            return {"message": msg}, 500

        sfields, sfield_relations = self._get_serializations("get")

        if item:
            result = item.to_dict(
                serial_fields=sfields, serial_field_relations=sfield_relations,
            )

            logger.debug(result)

            return result, 200

        msg = f"{name} with {key_name} of {key} not found"
        logger.debug(msg)
        return {"error": {"message": msg,}}, 404

    def post(self):
        """ Post """
        if request.is_json:
            data = request.json
        elif request.values:
            data = request.values
        elif request.data:
            data = request.data
        else:
            # running out of possibilities here
            data = request.args

        status, data = self.screen_data(
            self.model_class.deserialize(data), self.get_obj_params()
        )
        if status is False:
            return {"message": data}, 400

        key_name = self.get_key(formatted=False)
        name = self.model_class._class()

        if key_name in data:
            key = data[key_name]
            try:
                item = self.model_class.query.get(key)
            except:
                url = request.path
                msg = f"Internal Server Error: method post: {url}"
                logger.error(msg)
                return {"message": msg}, 500

            if item:
                return {"message": f"{key} for {name} already exists."}, 409

        item = self.model_class(**data)

        status, errors = item.validate_record(camel_case=True)

        item = self.pre_commit(item)

        try:
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

        item = self.post_commit(item)

        ser_list, rel_ser_lists = self._get_serializations("post")

        return (
            item.to_dict(
                serial_fields=ser_list, serial_field_relations=rel_ser_lists,
            ),
            201,
        )

    def put(self, **kwargs):
        """ put

        """
        try:
            key_name, key = self._check_key(kwargs)
        except Exception as err:
            logger.error(err.args[0])
            return {"message": err.args[0]}, 400

        try:
            item = self.model_class.query.get(key)
        except:
            url = request.path
            msg = f"Internal Server Error: method put: {url}"
            logger.error(msg)
            return {"message": msg}, 500

        if request.is_json:
            data = request.json
        elif request.values:
            data = request.values
        elif request.data:
            data = request.data
        else:
            data = request.args

        self.model_class.deserialize(data)

        # use the key from the url
        data[key_name] = key

        status, data = self.screen_data(data, self.get_obj_params())
        if status is False:
            return {"message": data}, 400

        if item is None:
            item = self.model_class(**data)
        else:
            for key, value in data.items():
                setattr(item, key, value)

        status, errors = item.validate_record(camel_case=True)

        item = self.pre_commit(item)
        try:
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
                {"message": f"An error occurred updating the {name}."},
                500,
            )

        item = self.post_commit(item)

        ser_list, rel_ser_lists = self._get_serializations("put")

        return (
            item.to_dict(
                serial_fields=ser_list, serial_field_relations=rel_ser_lists,
            ),
            201,
        )

        return data, 400

    def patch(self, **kwargs):
        """ Patch

        """
        name = self.model_class._class()

        try:
            key_name, key = self._check_key(kwargs)
        except Exception as err:
            logger.error(err.args[0])
            return {"message": err.args[0]}, 400

        try:
            item = self.model_class.query.get(key)
        except:
            url = request.path
            msg = f"Internal Server Error: method patch: {url}"
            logger.error(msg)
            return {"message": msg}, 500

        if request.is_json:
            data = request.json
        elif request.values:
            data = request.values
        elif request.data:
            data = request.data
        else:
            data = request.args

        self.model_class.deserialize(data)

        # use the key from the url
        data[key_name] = key
        status, data = self.screen_data(
            data, self.get_obj_params(), skip_missing_data=True
        )
        if status is False:
            return {"message": data}, 400

        if item is None:
            item = self.model_class(**data)
        else:
            for key, value in data.items():
                setattr(item, key, value)

        status, errors = item.validate_record(camel_case=True)

        item = self.pre_commit(item)
        try:
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
                {"message": f"An error occurred updating the {name}."},
                500,
            )

        item = self.post_commit(item)

        ser_list, rel_ser_lists = self._get_serializations("put")

        return (
            item.to_dict(
                serial_fields=ser_list, serial_field_relations=rel_ser_lists,
            ),
            201,
        )

        return data, 400

    def delete(self, **kwargs):
        """ Delete
        """
        name = self.model_class._class()

        try:
            key_name, key = self._check_key(kwargs)
        except Exception as err:
            logger.error(err.args[0])
            return {"message": err.args[0]}, 400

        try:
            item = self.model_class.query.get(key)
        except:
            url = request.path
            msg = f"Internal Server Error: method delete: {url}"
            logger.error(msg)
            return {"message": msg}, 500

        if item is None:
            msg = f"{name} with {key_name} of {key} not found"
            logger.debug(msg)
            return {"error": {"message": msg,}}, 404

        item = self.pre_commit(item)
        try:
            item.delete()
        except IntegrityError as err:
            # may be helpful
            msg = str(err).split("\n")[0]
            self.model_class.db.session.rollback()
            return {"message": msg}, 400

        except Exception as err:
            name = self.model_class._class()
            self.model_class.db.session.rollback()
            return (
                {"message": f"An error occurred deleting the {name}."},
                500,
            )

        msg = f"{name} with {key_name} of {key} is deleted"
        return {"message": msg}, 200
