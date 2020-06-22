# flask_restful_dbbase/resources/model_resource.py
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

    **Class variables**:

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

    process_get_input = None
    process_post_input = None
    process_put_input = None
    process_patch_input = None
    process_delete_input = None

    def get(self, **kwargs):
        """ Get """
        url = request.path
        FUNC_NAME = "get"
        name = self.model_class._class()

        # the correct key test - raises error if improper url
        key_name, key = self._check_key(kwargs)

        # for use only with self.process_get_input
        data = request.args

        query = self.model_class.query
        if self.process_get_input is not None:
            # 3 ways to end this
            # success: result is an updated query
            # failure:
            #   exit with a tuple that is a
            #       (message, status_code)
            #   exit with message, 500 error
            status, result = self.process_get_input(query, data, kwargs)
            if status is False:
                if isinstance(result, tuple):
                    return result
                else:
                    func = self.process_get_input.__name__
                    msg =  f"malformed error in {func}: {result}"
                    return { "message": msg}, 500

            query, data = result
        try:
            item = query.filter(
                getattr(self.model_class, key_name) == key
            ).first()

        except Exception as err:
            msg = err.args[0]
            return_msg = f"Internal Server Error: method {FUNC_NAME}: {url}"
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 500

        sfields, sfield_relations = self._get_serializations(FUNC_NAME)

        if item:
            result = item.to_dict(
                serial_fields=sfields, serial_field_relations=sfield_relations,
            )

            logger.debug(result)

            return result, 200

        msg = f"{name} with {key_name} of {key} not found"
        logger.debug(msg)
        return {"message": msg}, 404

    def post(self):
        """ Post """
        FUNC_NAME = "post"
        url = request.path
        status_code = 201
        if request.is_json:
            try:
                data = request.json
            except Exception as err:
                msg = err
                return_msg = f"A JSON format problem:{msg}: {request.data}"
                return {"message": return_msg}, 400
        elif request.values:
            data = request.values
        elif request.data:
            data = request.data
        else:
            data = request.args

        if self.process_post_input is not None:
            status, result = self.process_post_input(data)

            if status is False:
                # exit the scene, result should be a
                # tuple of message and status
                if isinstance(result, tuple):
                    return result
                else:
                    func = self.process_post_input.__name__
                    msg =  f"malformed error in {func}: {result}"
                    return { "message": msg}, 500

            data = result

        status, data = self.screen_data(self.model_class.deserialize(data))
        if status is False:
            return {"message": data}, 400

        key_name = self.get_key(formatted=False)
        name = self.model_class._class()

        if key_name in data:
            key = data[key_name]
            try:
                item = self.model_class.query.get(key)
            except Exception as err:
                msg = err.args[0]
                return_msg = f"Internal Server Error: method {FUNC_NAME}: "
                f"{url}"
                logger.error(f"{url} method {FUNC_NAME}: {msg}")
                return {"message": return_msg}, 500

            if item:
                return {"message": f"{key} for {name} already exists."}, 409

        item = self.model_class(**data)

        status, errors = item.validate_record(camel_case=True)

        adjust_before = self.before_commit.get(FUNC_NAME)
        if adjust_before is not None:
            if callable(adjust_before):
                item, status_code = adjust_before(self, item, status_code)
            else:
                item, status_code = adjust_before.run(self, item, status_code)

        try:
            item.save()
        except IntegrityError as err:
            # may be helpful
            msg = err.args[0]
            self.model_class.db.session.rollback()
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": msg}, 400

        except Exception as err:
            self.model_class.db.session.rollback()
            msg = err.args[0]
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return_msg = f"An error occurred inserting the {name}."
            return {"message": return_msg}, 500

        adjust_after = self.after_commit.get(FUNC_NAME)
        if adjust_after is not None:
            if callable(adjust_after):
                item, status_code = adjust_after(self, item, status_code)
            else:
                # class, requires a run function
                item, status_code = adjust_after.run(self, item, status_code)

        ser_list, rel_ser_lists = self._get_serializations(FUNC_NAME)

        return (
            item.to_dict(
                serial_fields=ser_list, serial_field_relations=rel_ser_lists,
            ),
            status_code,
        )

    def put(self, **kwargs):
        """ put

        """
        url = request.path
        FUNC_NAME = "put"
        status_code = 200
        try:
            key_name, key = self._check_key(kwargs)
        except Exception as err:
            # NOTE: error check this
            msg = err.args[0]
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": msg}, 400

        if request.is_json:
            try:
                data = request.json
            except Exception as err:
                msg = err
                return_msg = f"A JSON format problem:{msg}: {request.data}"
                return {"message": return_msg}, 400
        elif request.values:
            data = request.values
        elif request.data:
            data = request.data
        else:
            data = request.args

        query = self.model_class.query
        if self.process_put_input is not None:
            status, result = self.process_put_input(query, data, kwargs)

            if status is False:
                # exit the scene, data should be a
                # tuple of message and status
                if isinstance(result, tuple):
                    return result
                else:
                    func = self.process_put_input.__name__
                    msg =  f"malformed error in {func}: {result}"
                    return { "message": msg}, 500

            query, data = result

        try:
            item = query.filter(
                getattr(self.model_class, key_name) == key
            ).first()
        except Exception as err:
            msg = err.args[0]
            return_msg = f"Internal Server Error: method {FUNC_NAME}: {url}"
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 500

        data = self.model_class.deserialize(data)

        # use the key from the url
        data[key_name] = key
        status, data = self.screen_data(data)
        if status is False:
            return {"message": data}, 400

        if item is None:
            item = self.model_class(**data)
        else:
            for key, value in data.items():
                setattr(item, key, value)

        status, errors = item.validate_record(camel_case=True)
        adjust_before = self.before_commit.get(FUNC_NAME)
        if adjust_before is not None:
            if callable(adjust_before):
                item, status_code = adjust_before(self, item, status_code)
            else:
                item, status_code = adjust_before.run(self, item, status_code)

        try:
            item.save()
        except IntegrityError as err:
            msg = err.args[0]
            self.model_class.db.session.rollback()
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": msg}, 400

        except Exception as err:
            self.model_class.db.session.rollback()
            msg = err.args[0]
            return_msg = f"Internal Server Error: method {FUNC_NAME}: {url}"
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 500

        adjust_after = self.after_commit.get(FUNC_NAME)
        if adjust_after is not None:
            if callable(adjust_after):
                item, status_code = adjust_after(self, item, status_code)
            else:
                # class, requires a run function
                item, status_code = adjust_after.run(self, item, status_code)

        ser_list, rel_ser_lists = self._get_serializations(FUNC_NAME)

        return (
            item.to_dict(
                serial_fields=ser_list, serial_field_relations=rel_ser_lists,
            ),
            status_code,
        )

        return data, 400

    def patch(self, **kwargs):
        """ Patch

        """
        url = request.path
        FUNC_NAME = "patch"
        status_code = 200
        name = self.model_class._class()

        try:
            key_name, key = self._check_key(kwargs)
        except Exception as err:
            msg = err.args[0]
            logger.error(f"{url} method {FUNC_NAME}: {msg}")

            return {"message": msg}, 400

        if request.is_json:
            try:
                data = request.json
            except Exception as err:
                msg = err
                return_msg = f"A JSON format problem:{msg}: {request.data}"
                return {"message": return_msg}, 400
        elif request.values:
            data = request.values
        elif request.data:
            data = request.data
        else:
            data = request.args

        query = self.model_class.query
        if self.process_patch_input is not None:
            status, result = self.process_patch_input(query, data, kwargs)

            if status is False:
                # exit the scene, data should be a
                # tuple of message and status
                if isinstance(result, tuple):
                    return result
                else:
                    func = self.process_patch_input.__name__
                    msg =  f"malformed error in {func}: {result}"
                    return { "message": msg}, 500

            query, data = result

        try:
            item = query.filter(
                getattr(self.model_class, key_name) == key
            ).first()
        except Exception as err:
            msg = err.args[0]
            return_msg = f"Internal Server Error: method {FUNC_NAME}: {url}"
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 500

        data = self.model_class.deserialize(data)

        # use the key from the url
        data[key_name] = key
        status, data = self.screen_data(data, skip_missing_data=True)
        if status is False:
            return {"message": data}, 400

        if item is None:
            item = self.model_class(**data)
        else:
            for key, value in data.items():
                setattr(item, key, value)

        status, errors = item.validate_record(camel_case=True)

        adjust_before = self.before_commit.get(FUNC_NAME)
        if adjust_before is not None:
            if callable(adjust_before):
                item, status_code = adjust_before(self, item, status_code)
            else:
                item, status_code = adjust_before.run(self, item, status_code)

        try:
            item.save()
        except IntegrityError as err:
            msg = err.args[0]
            self.model_class.db.session.rollback()
            return {"message": msg}, 400

        except Exception as err:
            msg = err.args[0]
            self.model_class.db.session.rollback()
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return (
                {"message": f"An error occurred updating the {name}."},
                500,
            )

        adjust_after = self.after_commit.get(FUNC_NAME)
        if adjust_after is not None:
            if callable(adjust_after):
                item, status_code = adjust_after(self, item, status_code)
            else:
                # class, requires a run function
                item, status_code = adjust_after.run(self, item, status_code)

        ser_list, rel_ser_lists = self._get_serializations(FUNC_NAME)

        return (
            item.to_dict(
                serial_fields=ser_list, serial_field_relations=rel_ser_lists,
            ),
            status_code,
        )

        return data, 400

    def delete(self, **kwargs):
        """ Delete
        """
        url = request.path
        FUNC_NAME = "delete"
        status_code = 200
        name = self.model_class._class()

        try:
            key_name, key = self._check_key(kwargs)
        except Exception as err:
            logger.error(err.args[0])
            return {"message": err.args[0]}, 400

        query = self.model_class.query
        if self.process_delete_input is not None:
            status, result = self.process_delete_input(query, kwargs)

            if status is False:
                # exit the scene, data should be a
                # tuple of message and status
                if isinstance(result, tuple):
                    return result
                else:
                    func = self.process_delete_input.__name__
                    msg =  f"malformed error in {func}: {result}"
                    return { "message": msg}, 500

            query = result

        try:
            item = query.filter(
                getattr(self.model_class, key_name) == key
            ).first()
        except Exception as err:
            msg = err.args[0]
            return_msg = f"Internal Server Error: method "
            f"{FUNC_NAME}: {url}: {msg}"
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 500

        if item is None:
            msg = f"{name} with {key_name} of {key} not found"
            logger.debug(msg)
            return {"message": msg}, 404

        adjust_before = self.before_commit.get(FUNC_NAME)
        if adjust_before is not None:
            if callable(adjust_before):
                item, status_code = adjust_before(self, item, status_code)
            else:
                item, status_code = adjust_before.run(self, item, status_code)

        try:
            item.delete()
        except IntegrityError as err:
            self.model_class.db.session.rollback()
            msg = err.args[0]
            return_msg = f"Internal Server Error: method {FUNC_NAME}: {url}"
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": return_msg}, 400

        except Exception as err:
            name = self.model_class._class()
            self.model_class.db.session.rollback()
            msg = err.args[0]
            logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return (
                {"message": f"An error occurred deleting the {name}: {msg}."},
                500,
            )

        msg = f"{name} with {key_name} of {key} is deleted"
        return {"message": msg}, status_code
