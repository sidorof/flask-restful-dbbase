# tests/test_collection_model_resource.py
"""
This module tests collections.
"""
import unittest
from random import randint
import logging
import json
import uuid

import flask
import flask_restful
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import CollectionModelResource
from flask_restful_dbbase.validations import validate_process
from sqlalchemy import desc


logging.disable(logging.CRITICAL)


def create_samples(db):
    """
    create sample samples that have permissions on owner_id
    """

    class Sample(db.Model):
        __tablename__ = "sample"
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        owner_id = db.Column(db.Integer, nullable=False)
        param1 = db.Column(db.Integer, nullable=False)
        param2 = db.Column(db.String, nullable=False)
        status_id = db.Column(db.SmallInteger, default=0, nullable=True)

    db.create_all()

    # sample data
    for i in range(100):
        Sample(
            owner_id=randint(1, 3),
            param1=randint(1, 100),
            param2=str(uuid.uuid4()),
            status_id=randint(0, 5),
        ).save()

    return Sample


class TestCollectionModelResource(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This doesn't check defaults.'
        """
        app = flask.Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        api = flask_restful.Api(app)
        db = DBBase(app)
        cls.needs_setup = True

        @classmethod
        def set_db(cls):
            Sample = create_samples(db)
            cls.Sample = Sample

            class SampleCollectionResource(CollectionModelResource):
                model_class = cls.Sample
                process_get_input = None
                order_by = None
                max_page_size = None

            cls.api.add_resource(
                SampleCollectionResource, *SampleCollectionResource.get_urls()
            )

            class Sample1CollectionResource(CollectionModelResource):
                model_class = cls.Sample
                order_by = "status_id"
                max_page_size = 5

                def process_get_input(self, qry, data):
                    """Sets the status_id to 6 for no good reason."""
                    data["status_id"] = 6
                    return {
                        "status": True,
                        "query": qry,
                        "data": data
                    }

            cls.api.add_resource(Sample1CollectionResource, "/samples1")
            cls.needs_setup = False

            class Sample2CollectionResource(CollectionModelResource):
                model_class = cls.Sample
                order_by = ["status_id"]

                def process_get_input(self, qry, data):
                    """Returns True/False, depending on status."""

                    # use explicit variables to make it easier to validate
                    if "set_status" in data:
                        status = data.pop("set_status")[0]
                        if status == "good True status":\
                            return {
                                "status": True,
                                "query": qry,
                                "data": data
                            }
                        elif status == "bad True status":
                            return {
                                "status": True
                            }

                        elif status == "good False status":
                            return {
                                "status": False,
                                "message": status,
                                "status_code": 400
                            }
                        elif status == "bad False status":
                            return {
                                "status": False,
                                "message": status,
                            }
                        else:
                            # missing status
                            return "something else"

                    return {"status": True, "query": qry, "data": data}

            cls.api.add_resource(Sample2CollectionResource, "/samples2")
            cls.needs_setup = False

            # to test directly
            cls.Sample2CollectionResource = Sample2CollectionResource

        headers = {"Content-Type": "application/json"}
        cls.set_db = set_db
        cls.app = app
        cls.api = api
        cls.db = db
        cls.headers = headers

    @classmethod
    def tearDownClass(cls):
        cls.db.session.rollback()
        cls.db.session.remove()
        cls.db.Model.metadata.clear()
        cls.db = None
        del cls.db

    def test_model_name(self):
        db = self.db

        class TestModel(db.Model):
            __tablename__ = "test"
            id = db.Column(db.Integer, primary_key=True)

        class TestResource(CollectionModelResource):
            pass

        self.assertRaises(ValueError, TestResource)
        TestResource.model_class = TestModel

        self.assertEqual(TestResource().model_name, "TestModel")

    def test_is_collection(self):
        class SampleCollection(CollectionModelResource):
            model_class = self.Sample

        self.assertTrue(SampleCollection.is_collection())

    def test_get_urls(self):
        class ACollectionResource(CollectionModelResource):
            pass

        self.assertRaises(ValueError, ACollectionResource.get_urls)

    def test_get_no_params(self):
        """test_get_no_params"""
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get("/samples", headers=self.headers)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(len(res.get_json()[self.Sample._class()]), 100)
            self.assertEqual(
                list(res.get_json().keys())[0], self.Sample._class()
            )
            self.assertEqual(res.content_type, "application/json")

    def test__validate_process(self):

        class TestResource(CollectionModelResource):
            pass
            # model_class = self.Sample

        output = "not dict"

        self.assertRaises(
            ValueError,
            validate_process,
            output,
            true_keys=["query", "data"]
        )

        # missing status
        output = {}
        self.assertRaises(
            ValueError,
            validate_process,
            output,
            true_keys=["query", "data"]
        )

        # invalid status
        output = {"status": "hi there"}
        self.assertRaises(
            ValueError,
            validate_process,
            output,
            true_keys=["query", "data"]
        )

        # True status, no query, data
        output = {"status": True}
        self.assertRaises(
            ValueError,
            validate_process,
            output,
            true_keys=["query", "data"]
        )
        # True status, with query, no data
        output = {"status": True, "query": "stuff"}
        self.assertRaises(
            ValueError,
            validate_process,
            output,
            true_keys=["query", "data"]
        )
        # True status, with query and data, no validation on type
        output = {"status": True, "query": "stuff", "data": "stuff"}
        self.assertIsNone(
            validate_process(
                output,
                true_keys=["query", "data"]
            )
        )

        # False status, no message, status_code
        output = {"status": False}
        self.assertRaises(
            ValueError,
            validate_process,
            output,
            true_keys=["query", "data"]
        )
        # False status, with message, no status_code
        output = {"status": False, "message": "stuff"}
        self.assertRaises(
            ValueError,
            validate_process,
            output,
            true_keys=["query", "data"]
        )
        # False status, with message and status_code, no validation on type
        output = {"status": False, "message": "stuff", "status_code": 400}
        self.assertIsNone(
            validate_process(
                output,
                true_keys=["query", "data"]
            )
        )



    def test__page_configs(self):

        db = self.db

        class TestModel(db.Model):
            __tablename__ = "test_page_configs"
            id = db.Column(db.Integer, primary_key=True)

        class PageConfigCollection(CollectionModelResource):
            model_class = TestModel
            max_page_size = 20

        class_resource = PageConfigCollection()

        sample_config = {
            "orderBy": ["id", "statusId"],
            "pageSize": "50",
            "offset": 30,
            "limit": "100",
            "debug": "False",
            "serialFields": ["id", "statusId"],
        }

        configs = class_resource._page_configs(sample_config)

        self.assertDictEqual(
            configs,
            {
                "order_by": ["id", "status_id"],
                "page_size": 20,  # reduced because of max_page_size
                "offset": 30,
                "limit": 100,
                "debug": False,
                "serial_fields": ["id", "status_id"],
            },
        )

        sample_config = {
            "debug": "True"
        }

        configs = class_resource._page_configs(sample_config)

        self.assertDictEqual(
            configs,
            {
                "debug": True
            }
        )

        sample_config = {
            "badvar": "test"
        }

        self.assertRaises(
            ValueError,
            class_resource._page_configs, sample_config
        )

        sample_config = {}
        class_resource.order_by = "id"

        configs = class_resource._page_configs(sample_config)

        self.assertDictEqual(
            configs,
            {
                "order_by": ["id"]
            }
        )

    def test_config_params_order(self):
        """
        Test configuration of the records being returned.

        These are found in a _config dict. Such a name is to
        avoid name polution of the query variables.

        page_config = {
            page_size: None | value,
            offset: None | value
            debug: boolean,
            order_by: value | array,
            serial_fields: array,
            # serial_field_relations  not addressed
        }

        variables = {
            field1: value,              select if field1 == value
            field2[]: array  in list    select field2 with values in array

            field3: [operator, value]   eq, gt, lt, ne, like

        }
        """
        # sorted in numerical order
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples",
                query_string={
                    "ownerId[]": [1, 3],
                    "pageConfig": {
                        "orderBy": ["id", "statusId"],
                        "pageSize": 20,
                        "offset": 30,
                        # booleans have to be strings
                        # NOTE: see how it looks from axios
                        "debug": "false",
                        "serialFields": ["id", "statusId"],
                    },
                },
                headers=self.headers,
            )
            Sample = self.Sample
            qry = (
                Sample.query
                    .filter(Sample.owner_id.in_([1, 3]))
                    .order_by(Sample.id, Sample.status_id)
                    .offset(30)
                    .limit(20)
                    .all()
            )

            tmp = res.json

            self.assertEqual(res.status_code, 200)

            tmp1 = [
                sample.to_dict(serial_fields=["id", "status_id"])
                for sample in qry
            ]

            self.assertEqual(
                len(res.get_json()[Sample._class()]),
                len(qry),
            )

            self.assertListEqual(
                res.get_json()[Sample._class()],
                tmp1
            )

            self.assertEqual(res.content_type, "application/json")

    def test_config_params_order_reverse(self):
        # sorted in descending numerical order
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples",
                query_string={
                    "ownerId[]": [1, 3],
                    "pageConfig": {"orderBy": ["-id"]},
                },
                headers=self.headers,
            )
            Sample = self.Sample

            qry = (
                Sample.query
                    .filter(Sample.owner_id.in_([1, 3]))
                    .order_by(Sample.id.desc())
                    .all()
            )

            tmp = res.json
            self.assertEqual(res.status_code, 200)

            tmp1 = [sample.to_dict() for sample in qry]

            self.assertEqual(
                len(res.get_json()[Sample._class()]),
                len(qry),
            )

            self.assertListEqual(
                res.get_json()[Sample._class()],
                tmp1
            )

            self.assertEqual(res.content_type, "application/json")

    def test_config_params_order_with_vars(self):
        # compare to a another column variable
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples",
                query_string={
                    "ownerId": ["gt", "var:statusId"],
                    "pageConfig": {"orderBy": ["-id"]},
                },
                headers=self.headers,
            )

            Sample = self.Sample
            qry = (
                Sample.query
                    .filter(Sample.owner_id.__gt__(Sample.status_id))
                    .order_by(Sample.id.desc())
                    .all()
            )

            tmp = res.json
            self.assertEqual(res.status_code, 200)

            tmp1 = [sample.to_dict() for sample in qry]

            self.assertEqual(
                len(res.get_json()[Sample._class()]),
                len(qry),
            )

            self.assertListEqual(
                res.get_json()[Sample._class()],
                tmp1
            )

            self.assertEqual(res.content_type, "application/json")

    def test_config_params_order_single(self):
        # variable not in a list
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples",
                query_string={
                    "ownerId[]": [1, 3],
                    "pageConfig": {"orderBy": "-id"},
                },
                headers=self.headers,
            )
            Sample = self.Sample
            qry = (
                Sample.query
                    .filter(Sample.owner_id.in_([1, 3]))
                    .order_by(Sample.id.desc())
                    .all()
            )

            tmp = res.json
            self.assertEqual(res.status_code, 200)

            tmp1 = [sample.to_dict() for sample in qry]

            self.assertEqual(
                len(res.get_json()[Sample._class()]),
                len(qry),
            )

            self.assertListEqual(
                res.get_json()[Sample._class()],
                tmp1
            )

            self.assertEqual(res.content_type, "application/json")

    def test_config_params_op_codes1(self):

        # test OP_CODES
        # test like, ilike, notilike  separately
        op_codes = ["eq", "ne", "gt", "ge", "lt", "le"]
        value = 50

        for op in op_codes:

            with self.app.test_client() as client:
                if self.needs_setup:
                    self.set_db()

                res = client.get(
                    "/samples",
                    query_string={"param1": [op, value]},
                    headers=self.headers,
                )
                Sample = self.Sample

                func = getattr(Sample.param1, f"__{op}__")
                qry = Sample.query .filter(func(value)).all()

                res_qry = res.json
                self.assertEqual(res.status_code, 200)

                db_qry = [sample.to_dict() for sample in qry]
                self.assertEqual(
                    len(res_qry[Sample._class()]),
                    len(db_qry),
                )
                self.assertEqual(
                    res_qry[Sample._class()],
                    db_qry
                )

                self.assertEqual(res.content_type, "application/json")

    def test_config_params_missing_value1(self):

        # test OP_CODES
        # test like, ilike, notilike  separately
        op_codes = ["eq", "ne", "gt", "ge", "lt", "le"]

        for op in op_codes:

            with self.app.test_client() as client:
                if self.needs_setup:
                    self.set_db()

                res = client.get(
                    "/samples",
                    query_string={"param1": [op]},
                    headers=self.headers,
                )

                res_qry = res.json

                self.assertEqual(res.status_code, 400)

    def test_config_params_op_codes2(self):
        op_codes = ["like", "ilike", "notilike"]
        value = "\\%f\\%"

        for op in op_codes:

            with self.app.test_client() as client:
                if self.needs_setup:
                    self.set_db()

                res = client.get(
                    "/samples",
                    query_string={"param2": [op, value]},
                    headers=self.headers,
                )
                Sample = self.Sample

                func = getattr(Sample.param2, op)
                qry = Sample.query .filter(func(value))
                qry = qry.all()

                res_qry = res.json
                self.assertEqual(res.status_code, 200)

                db_qry = [sample.to_dict() for sample in qry]
                self.assertEqual(
                    len(res_qry[Sample._class()]),
                    len(db_qry),
                )
                self.assertEqual(
                    res_qry[Sample._class()],
                    db_qry
                )

                self.assertEqual(res.content_type, "application/json")

    def test_config_params_missing_value2(self):
        op_codes = ["like", "ilike", "notilike"]
        value = "[]"

        for op in op_codes:

            with self.app.test_client() as client:
                if self.needs_setup:
                    self.set_db()

                res = client.get(
                    "/samples",
                    query_string={"param2": [op]},
                    headers=self.headers,
                )
                res_qry = res.json
                self.assertEqual(res.status_code, 400)

    def test_config_params_unknown_op(self):
        op_codes = ["bad"]
        value = "\\%f\\%"

        for op in op_codes:

            with self.app.test_client() as client:
                if self.needs_setup:
                    self.set_db()

                res = client.get(
                    "/samples",
                    query_string={"param2": [op, value]},
                    headers=self.headers,
                )

                res_qry = res.json
                self.assertEqual(res.status_code, 400)

    def test_config_params_simple_eq(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples",
                query_string={"id": 40},
                headers=self.headers,
            )

            Sample = self.Sample

            qry = Sample.query .filter(Sample.id == 40)
            qry = qry.all()

            res_qry = res.json
            self.assertEqual(res.status_code, 200)

            db_qry = [sample.to_dict() for sample in qry]
            self.assertEqual(
                len(res_qry[Sample._class()]),
                len(db_qry),
            )
            self.assertEqual(
                res_qry[Sample._class()],
                db_qry
            )

            self.assertEqual(res.content_type, "application/json")

    def test_config_params_debug1(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples1",
                query_string={
                    "id": 40,
                    "pageConfig": {
                        "debug": "True"
                    }
                },
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 200)

            self.assertDictEqual(
                res_qry,
                {
                "class_defaults": {
                    "model_name": "Sample",
                    "process_get_input": "Sets the status_id to 6 for no good reason.",
                    "max_page_size": 5,
                    "order_by": None,
                    "op_codes": [
                        "eq",
                        "ne",
                        "gt",
                        "ge",
                        "lt",
                        "le",
                        "like",
                        "ilike",
                        "notlike",
                        "notilike"
                    ]
                },
                "original_data": {
                    "id": [
                        "40"
                    ],
                    "pageConfig": [
                        "{'debug': 'True'}"
                    ]
                },
                "converted_data": [
                    [
                        "id",
                        "eq",
                        [
                            "40"
                        ]
                    ],
                    [
                        "status_id",
                        "eq",
                        6
                    ]
                ],
                "page_configs": {
                    "debug": True,
                    "order_by": [
                        "status_id"
                    ]
                },
                "query": "SELECT sample.id AS sample_id, sample.owner_id AS sample_owner_id, sample.param1 AS sample_param1, sample.param2 AS sample_param2, sample.status_id AS sample_status_id \nFROM sample \nWHERE sample.id IN (?) AND sample.status_id = ? ORDER BY sample.status_id"
                }
            )

    def test_config_params_debug2(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples",
                query_string={
                    "id": 40,
                    "pageConfig": {
                        "debug": "True",
                        "limit": 40

                    }
                },
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 200)

            self.assertDictEqual(
                res_qry,
                {
                    "class_defaults": {
                        "model_name": "Sample",
                        "process_get_input": None,
                        "max_page_size": None,
                        "order_by": None,
                        "op_codes": [
                            "eq",
                            "ne",
                            "gt",
                            "ge",
                            "lt",
                            "le",
                            "like",
                            "ilike",
                            "notlike",
                            "notilike"
                        ]
                    },
                    "original_data": {
                        "id": [
                            "40"
                        ],
                        "pageConfig": [
                            "{'debug': 'True', 'limit': 40}"
                        ]
                    },
                    "converted_data": [
                        [
                            "id",
                            "eq",
                            [
                                "40"
                            ]
                        ]
                    ],
                    "page_configs": {
                        "debug": True,
                        "limit": 40
                    },
                    "query": "SELECT sample.id AS sample_id, sample.owner_id AS sample_owner_id, sample.param1 AS sample_param1, sample.param2 AS sample_param2, sample.status_id AS sample_status_id \nFROM sample \nWHERE sample.id IN (?)\n LIMIT ? OFFSET ?"
                }
            )

    def test_config_params_invalid_order_var(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples",
                query_string={
                    "id": 40,
                    "pageConfig": {
                        "debug": "True",
                        "orderBy": "test"

                    }
                },
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res_qry,
                {'message': 'test is not a column in Sample'}
            )

        # now with descending order
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples",
                query_string={
                    "id": 40,
                    "pageConfig": {
                        "debug": "True",
                        "orderBy": "-test"

                    }
                },
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res_qry,
                {'message': 'test is not a column in Sample'}
            )

    def test_config_params_fmt_of_class_order_var(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples2",
                query_string={
                    "set_status": "good True status",
                    "pageConfig": {
                        "debug": "True",
                    }
                },
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 200)

            self.assertDictEqual(
                res_qry,
                {
                    "class_defaults": {
                        "model_name": "Sample",
                        "process_get_input": "Returns True/False, depending on status.",
                        "max_page_size": None,
                        "order_by": None,
                        "op_codes": [
                            "eq",
                            "ne",
                            "gt",
                            "ge",
                            "lt",
                            "le",
                            "like",
                            "ilike",
                            "notlike",
                            "notilike"
                        ]
                    },
                    "original_data": {
                        "set_status": [
                            "good True status"
                        ],
                        "pageConfig": [
                            "{'debug': 'True'}"
                        ]
                    },
                    "converted_data": [],
                    "page_configs": {
                        "debug": True,
                        "order_by": [
                            "status_id"
                        ]
                    },
                    "query": "SELECT sample.id AS sample_id, sample.owner_id AS sample_owner_id, sample.param1 AS sample_param1, sample.param2 AS sample_param2, sample.status_id AS sample_status_id \nFROM sample ORDER BY sample.status_id"
                }

            )

    def test_config_params_bad_input_process(self):

        # True, but not followed by tuple of (query, data)
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples2",
                query_string={"set_status": "bad True status"},
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)
        #
        # # True, good with correct tuple
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples2",
                query_string={"set_status": "good True status"},
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 200)

        # # False, good with correct tuple
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples2",
                query_string={"set_status": "good False status"},
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res_qry,
                {"message": "good False status"}
            )

        # # False, without correct message format
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples2",
                query_string={"set_status": "bad False status"},
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)
