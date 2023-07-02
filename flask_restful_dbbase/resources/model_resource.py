# flask_restful_dbbase/resources/model_resource.py
""""
This module implements a starting point for model resources.

"""
from flask import current_app
from flask_restful import request
from .dbbase_resource import DBBaseResource
from ..validations import validate_process


class ModelResource(DBBaseResource):
    """
    ModelResource Class

    This model class implements the base class.

    **Class variables**:

    model_class: a dbbase.Model


    url_prefix: the portion of the path leading up to the resource
        For example: /api/v2

    url_name: the url_name defaults to a lower case version of the
        the model_class name if left as None, but can have an
        explicit name if necessary.

    serial_fields: if left as None, it uses the serial list from
        the model class. However, it can be a list of field names
        or

    before_commit: A dict with method keys for placing a function
        to run just before committing an item to the database. It
        can also divert the method to end the HTTP method early and
        return something entirely different than the item being applied.

    after_commit: A dict with method keys for placing a function
        to run just afteer committing an item to the database. It
        can also divert the method to end the HTTP method early and
        return something entirely different than the item being applied.


    """

    process_get_input = None
    process_post_input = None
    process_put_input = None
    process_patch_input = None
    process_delete_input = None

    def get(self, **kwargs):
        """
        This function is the HTTP GET method for a resource handling
        a single item.
        """
        # may be used later
        # url = request.path
        FUNC_NAME = "get"

        # the correct key test - raises error if improper url
        current_app.logger.debug("Checking key in kwargs")
        kdict = self._check_key(kwargs)
        current_app.logger.debug(f"Completed key in kwargs: {kdict}")

        # for use only with self.process_get_input
        data = request.args.to_dict(flat=False)
        current_app.logger.debug(f"Request args: {data}")
        query = self.model_class.query
        if self.process_get_input is not None:
            try:
                current_app.logger.debug("function process_get_input started")
                output = self.process_get_input(query, data, kwargs)
            except Exception as err:
                current_app.logger.error(err.args)
                return "Failure in process_get_input function", 500

            current_app.logger.debug("function validate_process started")
            validate_process(output, true_keys=["query", "data"])
            current_app.logger.debug("function validate_process finished")

            if output["status"]:
                current_app.logger.debug(
                    "Output process_get_input status: True"
                )

                query = output["query"]
                data = output["data"]
                current_app.logger.debug(
                    "Processing continuing with updated query/data"
                )
            else:
                current_app.logger.debug("Output process_get_input status: False")
                message = output["message"]
                status_code = output["status_code"]

                current_app.logger.debug(f"{message}: {status_code}")
                return message, status_code

        try:
            for key_name, key in kdict.items():
                current_app.logger.debug(
                    f"query filtering with {key_name} == {key}"
                )
                query = query.filter(
                    getattr(self.model_class, key_name) == key
                )
            item = query.first()
            current_app.logger.debug(
                f"item {item} selected"
            )
        except Exception as err:
            msg = err.args[0]
            current_app.logger.error(msg)
            return {"message": msg}, 400

        sfields, sfield_relations = self._get_serializations(FUNC_NAME)
        current_app.logger.debug("Serial fields: {sfields}")
        current_app.logger.debug("Serial field relations: {sfield_relations}")
        if item:
            result = item.to_dict(
                serial_fields=sfields,
                serial_field_relations=sfield_relations,
            )

            current_app.logger.debug(result)

            return result, 200

        msg = f"{self.model_name} with {kdict} not found"
        current_app.logger.debug(msg)
        return {"message": msg}, 404

    def post(self):
        """
        This function is the HTTP POST method for a resource handling
        a single item.
        """
        FUNC_NAME = "post"
        # may be used later
        url = request.path
        status_code = 201

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

        if self.process_post_input is not None:
            current_app.logger.debug("function process_post_input started")
            output = self.process_post_input(data)
            current_app.logger.debug("Completed process_post_input")

            validate_process(output, true_keys=["data"])
            current_app.logger.debug("Completed validate_process function")

            if output["status"]:
                current_app.logger.debug("Output process_get_input status: True")
                data = output["data"]
            else:
                message = output["message"]
                status_code = output["status_code"]

                return message, status_code

        obj_params = self.get_obj_params()

        try:
            current_app.logger.debug(
                "Sceening/filtering data for unnecessary variables"
            )
            status, data = self.screen_data(
                self.model_class.deserialize(data), obj_params
            )
        except Exception as err:
            msg = f"malformed data: {err.args[0]}"
            current_app.logger.error(msg)
            return {"message": msg}, 400

        if status is False:
            current_app.logger.info(data)
            return {"message": data}, 400

        key_names = self.get_key_names(formatted=False)

        item = None

        current_app.logger.debug("Checking for key names/ids")
        status, kdict = self._all_keys_found(key_names, data)

        if status:
            # verify it does not already exist
            current_app.logger.debug("Verifying keys not already present")
            query = self.model_class.query
            for key_name, value in kdict.items():
                query = query.filter(
                    getattr(self.model_class, key_name) == value
                )
            try:
                item = query.first()
            except Exception as err:
                msg = err.args[0]
                current_app.logger.error(msg)
                return {"message": msg}, 400

        if item:
            msg = f"{kdict} for {self.model_name} already exists."
            current_app.logger.info(msg)
            return (
                {"message": msg},
                409,
            )

        non_rel_columns = dict(
            [
                [key, value]
                for key, value in obj_params.items()
                if "relationship" not in value
            ]
        )

        non_rel_data = dict(
            [
                [key, value]
                for key, value in data.items()
                if key in non_rel_columns
            ]
        )
        item = self.model_class(**non_rel_data)

        rel_columns = dict(
            [
                [key, value]
                for key, value in obj_params.items()
                if "relationship" in value
            ]
        )

        # relationship data by column
        rel_data = dict(
            [[key, value] for key, value in data.items() if key in rel_columns]
        )

        for key, value in rel_data.items():
            # key such as invoice_items
            rel_info = rel_columns[key]["relationship"]
            sub_obj_params = rel_info["fields"]
            entity = rel_info["entity"]
            sub_class = self.model_class._decl_class_registry[entity]

            if rel_info["type"] == "list":
                if not isinstance(value, list):
                    return (
                        {"message": f"{key} data must be in a list form"},
                        400,
                    )
                for subitem in value:
                    # subitem such as invoice item
                    # screen against column
                    # no missing data check, parent id auto filled
                    # NOTE: needs further work
                    sub_status, sub_data = self.screen_data(
                        self.model_class.deserialize(subitem),
                        sub_obj_params,
                        skip_missing_data=True,
                    )
                    if sub_status is False:
                        # NOTE: look at this further
                        current_app.logger.info(sub_data)
                        return {"message": sub_data}, 400

                    getattr(item, key).append(sub_class(**sub_data))

        adjust_before = self.before_commit.get(FUNC_NAME)

        if adjust_before is not None:
            current_app.logger.debug(
                "Running adjust_before function prior to commit"
            )
            status, result, status_code = self._item_adjust(
                adjust_before, item, status_code
            )
            if status:
                item = result
            else:
                current_app.logger.debug(
                    f"Return diverted: {result}: {status_code}"
                )
                return result, status_code

        try:
            current_app.logger.debug("Posting to database")
            item.save()
        except Exception as err:
            self.model_class.db.session.rollback()
            msg = err.args[0]
            current_app.logger.error(msg)
            current_app.logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": msg}, 400

        adjust_after = self.after_commit.get(FUNC_NAME)
        if adjust_after:
            current_app.logger.debug(
                "Running adjust_after function after commit"
            )
            status, result, status_code = self._item_adjust(
                adjust_after, item, status_code
            )
            if status:
                item = result
            else:
                current_app.logger.debug(
                    f"Return diverted: {result}: {status_code}"
                )
                return result, status_code

        ser_fields, rel_ser_fields = self._get_serializations(FUNC_NAME)

        return (
            item.to_dict(
                serial_fields=ser_fields,
                serial_field_relations=rel_ser_fields,
            ),
            status_code,
        )

    def put(self, **kwargs):
        """
        This function is the HTTP PUT method for a resource handling a
        single item.
        """
        url = request.path
        FUNC_NAME = "put"
        status_code = 200
        try:
            current_app.logger.debug("Checking key in kwargs")
            kdict = self._check_key(kwargs)
        except Exception as err:
            msg = err.args[0]
            current_app.logger.info(msg)
            return {"message": msg}, 400

        current_app.logger.debug(f"Completed key in kwargs: {kdict}")

        if request.is_json:
            try:
                data = request.json
            except Exception as err:
                msg = err
                return_msg = f"A JSON format problem:{msg}"
                current_app.logger.info(return_msg)
                return {"message": return_msg}, 400
        else:
            return {"message": "JSON format is required"}, 415

        query = self.model_class.query
        if self.process_put_input is not None:
            try:
                current_app.logger.debug("function process_put_input started")
                output = self.process_put_input(query, data, kwargs)
            except Exception as err:
                current_app.logger.error(err.args)

            current_app.logger.debug("function validate_process started")
            validate_process(output, true_keys=["query", "data"])
            current_app.logger.debug("function validate_process finished")

            if output["status"]:
                current_app.logger.debug(
                    "Output process_put_input status: True"
                )

                query = output["query"]
                data = output["data"]

                current_app.logger.debug(
                    "Processing continuing with updated query/data"
                )
            else:
                current_app.logger.debug("Output process_put_input status: False")
                message = output["message"]
                status_code = output["status_code"]

                current_app.logger.debug(f"{message}: {status_code}")
                return message, status_code

        status, kdict = self._all_keys_found(list(kdict.keys()), data)
        if status:
            for key_name, value in kdict.items():
                query = query.filter(
                    getattr(self.model_class, key_name) == value
                )
        try:
            item = query.first()

        except Exception as err:
            msg = err.args[0]
            current_app.logger.error(msg)
            return {"message": msg}, 400

        data = self.model_class.deserialize(data)

        # use the key(s) from the url
        data.update(kdict)

        obj_params = self.get_obj_params()

        try:
            current_app.logger.debug(
                "Sceening/filtering data for unnecessary variables"
            )
            status, data = self.screen_data(
                self.model_class.deserialize(data), obj_params
            )
        except Exception as err:
            msg = f"malformed data: {err.args[0]}"
            current_app.logger.error(msg)
            return {"message": msg}, 400

        if status is False:
            current_app.logger.info(f"{str(data)}: 400")
            return {"message": data}, 400

        if item is None:
            item = self.model_class(**data)
        else:
            for key, value in data.items():
                setattr(item, key, value)

        adjust_before = self.before_commit.get(FUNC_NAME)
        if adjust_before:
            current_app.logger.debug(
                "Running adjust_before function prior to commit"
            )
            status, result, status_code = self._item_adjust(
                adjust_before, item, status_code
            )
            if status:
                item = result
            else:
                current_app.logger.debug(
                    f"Return diverted: {result}: {status_code}"
                )
                return result, status_code

        try:
            current_app.logger.debug("Saving to database")
            item.save()

        except Exception as err:
            self.model_class.db.session.rollback()
            msg = err.args[0]
            self.model_class.db.session.rollback()
            current_app.logger.info(msg)
            current_app.logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return {"message": msg}, 400

        adjust_after = self.after_commit.get(FUNC_NAME)
        if adjust_after:
            current_app.logger.debug(
                "Running adjust_after function after commit"
            )
            status, result, status_code = self._item_adjust(
                adjust_after, item, status_code
            )
            if status:
                item = result
            else:
                current_app.logger.debug(
                    f"Return diverted: {result}: {status_code}"
                )
                return result, status_code

        ser_fields, rel_ser_fields = self._get_serializations(FUNC_NAME)

        return (
            item.to_dict(
                serial_fields=ser_fields,
                serial_field_relations=rel_ser_fields,
            ),
            status_code,
        )

    def patch(self, **kwargs):
        """
        This function is the HTTP PATCH method for a resource handling
        a single item.
        """
        url = request.path
        FUNC_NAME = "patch"
        status_code = 200

        try:
            current_app.logger.debug("Checking key in kwargs")
            kdict = self._check_key(kwargs)
        except Exception as err:
            msg = err.args[0]
            current_app.logger.info(msg)
            return {"message": msg}, 400

        current_app.logger.debug(f"Completed key in kwargs: {kdict}")

        if request.is_json:
            try:
                data = request.json
            except Exception as err:
                msg = err
                return_msg = f"A JSON format problem:{msg}: {request.data}"
                return {"message": return_msg}, 400
        else:
            return {"message": "JSON format is required"}, 415

        query = self.model_class.query
        if self.process_patch_input is not None:
            try:
                current_app.logger.debug("function process_patch_input started")
                output = self.process_patch_input(query, data, kwargs)
            except Exception as err:
                msg = f"{err.args}"
                current_app.logger.error(msg)
                return {"message": msg}, 500

            current_app.logger.debug("function validate_process started")
            validate_process(output, true_keys=["query", "data"])
            current_app.logger.debug("function validate_process finished")

            if output["status"]:
                current_app.logger.debug(
                    "Output process_put_input status: True"
                )

                query = output["query"]
                data = output["data"]

                current_app.logger.debug(
                    "Processing continuing with updated query/data"
                )
            else:
                current_app.logger.debug("Output process_put_input status: False")
                message = output["message"]
                status_code = output["status_code"]

                current_app.logger.debug(f"{message}: {status_code}")
                return message, status_code

        for key_name, value in kdict.items():
            query = query.filter(getattr(self.model_class, key_name) == value)

        try:
            item = query.first()
        except Exception as err:
            self.model_class.db.session.rollback()
            msg = err.args[0]
            current_app.logger.error(msg)
            return {"message": msg}, 400

        data = self.model_class.deserialize(data)

        data.update(kdict)
        obj_params = self.get_obj_params()

        try:
            current_app.logger.debug(
                "Sceening/filtering data for unnecessary variables"
            )
            status, data = self.screen_data(
                self.model_class.deserialize(data),
                obj_params,
                skip_missing_data=True
            )
        except Exception as err:
            msg = f"malformed data: {err.args[0]}"
            current_app.logger.error(msg)
            return {"message": msg}, 400

        if status is False:
            current_app.logger.info(f"{str(data)}: 400")
            return {"message": data}, 400

        if item is None:
            item = self.model_class(**data)
        else:
            for key, value in data.items():
                setattr(item, key, value)

        adjust_before = self.before_commit.get(FUNC_NAME)

        if adjust_before is not None:
            current_app.logger.debug(
                "Running adjust_before function prior to commit"
            )
            status, result, status_code = self._item_adjust(
                adjust_before, item, status_code
            )
            if status:
                item = result
            else:
                current_app.logger.debug(
                    f"Return diverted: {result}: {status_code}"
                )
                return result, status_code

        try:
            current_app.logger.debug("Saving to database")
            item.save()
        except Exception as err:
            msg = err.args[0]
            self.model_class.db.session.rollback()
            current_app.logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return (
                {
                    "message": "An error occurred updating the "
                    f"{self.model_name}: {msg}."
                },
                500,
            )

        adjust_after = self.after_commit.get(FUNC_NAME)
        if adjust_after:
            current_app.logger.debug(
                "Running adjust_after function after commit"
            )

            status, result, status_code = self._item_adjust(
                adjust_after, item, status_code
            )
            if status:
                item = result
            else:
                current_app.logger.debug(
                    f"Return diverted: {result}: {status_code}"
                )
                return result, status_code

        ser_fields, rel_ser_fields = self._get_serializations(FUNC_NAME)

        return (
            item.to_dict(
                serial_fields=ser_fields,
                serial_field_relations=rel_ser_fields,
            ),
            status_code,
        )

    def delete(self, **kwargs):
        """
        This function is the HTTP DELETE method for a resource
        handling a single item.
        """
        url = request.path
        FUNC_NAME = "delete"
        status_code = 200
        try:
            current_app.logger.debug("Checking key in kwargs")
            kdict = self._check_key(kwargs)
        except Exception as err:
            msg = err.args[0]
            return {"message": msg}, 400

        current_app.logger.debug(f"Completed key in kwargs: {kdict}")

        query = self.model_class.query
        if self.process_delete_input is not None:

            try:
                current_app.logger.debug("function process_delete_input started")
                output = self.process_delete_input(query, kwargs)
            except Exception as err:
                msg = f"{err.args}"
                current_app.logger.error(msg)
                return {"message": msg}, 500

            current_app.logger.debug("function validate_process started")
            validate_process(output, true_keys=["query"])
            current_app.logger.debug("function validate_process finished")

            if output["status"]:
                query = output["query"]
            else:
                message = output["message"]
                status_code = output["status_code"]

                return {"message": message}, status_code

        for key_name, value in kdict.items():
            query = query.filter(getattr(self.model_class, key_name) == value)

        try:
            item = query.first()
        except Exception as err:
            msg = err.args[0]
            current_app.logger.error(msg)
            return {"message": msg}, 500

        if item is None:
            msg = f"{self.model_name} with {kdict} not found"
            current_app.logger.debug(msg)
            return {"message": msg}, 404

        adjust_before = self.before_commit.get(FUNC_NAME)
        if adjust_before is not None:
            current_app.logger.debug(
                "Running adjust_before function prior to commit"
            )
            status, result, status_code = self._item_adjust(
                adjust_before, item, status_code
            )
            if status:
                item = result
            else:
                current_app.logger.debug(
                    f"Return diverted: {result}: {status_code}"
                )
                return result, status_code

        try:
            current_app.logger.debug("Deleting from database")
            item.delete()
        except Exception as err:
            self.model_class.db.session.rollback()
            msg = err.args[0]
            current_app.logger.error(f"{url} method {FUNC_NAME}: {msg}")
            return (
                {
                    "message": "An error occurred deleting the "
                    f"{self.model_name}: {msg}."
                },
                500,
            )

        msg = f"{self.model_name} with {kdict} is deleted"
        return {"message": msg}, status_code
