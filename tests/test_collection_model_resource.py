# tests/test_collection_model_resource.py
"""
This module tests collections.
"""
import unittest
from random import randint
import logging

import flask
import flask_restful
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import CollectionModelResource


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
        param2 = db.Column(db.Integer, nullable=False)
        status_id = db.Column(db.SmallInteger, default=0, nullable=True)

    db.create_all()

    # sample data
    for i in range(100):
        Sample(
            owner_id=randint(1, 3),
            param1=randint(1, 100),
            param2=randint(1, 100),
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
                process_get_input = None
                order_by = "status_id"
                max_page_size = 5

            cls.api.add_resource(Sample1CollectionResource, "/samples1")
            cls.needs_setup = False

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
        """ test_get_no_params

        """
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

    def test_get_with_params(self):
        """ test_get_with_params

        """
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.get(
                "/samples",
                query_string={
                    "ownerId": 1,
                    "orderBy": "statusId",
                    "debug": False,
                },
                headers=self.headers,
            )
            Sample = self.Sample
            qry = Sample.query.filter(Sample.owner_id == 1).all()

            self.assertEqual(res.status_code, 200)

            self.assertEqual(
                len(res.get_json()[Sample._class()]), len(qry),
            )
            self.assertEqual(res.content_type, "application/json")

            # invalid order column name
            res = client.get(
                "/samples",
                query_string={
                    "ownerId": 1,
                    "orderBy": "statusID",
                    "pageSize": 10,
                    "debug": False,
                },
                headers=self.headers,
            )

            self.assertDictEqual(
                res.get_json(),
                {"message": "status_i_d is not a column in Sample"},
            )

            self.assertEqual(res.status_code, 400)

            res = client.get(
                "/samples",
                query_string={
                    "ownerId": 1,
                    "orderBy": "statusId",
                    "pageSize": 10,
                    "debug": False,
                },
                headers=self.headers,
            )
            Sample = self.Sample
            qry = Sample.query.filter(Sample.owner_id == 1).limit(10).all()

            self.assertEqual(res.status_code, 200)

            self.assertEqual(
                len(res.get_json()[Sample._class()]), len(qry),
            )

            # multiple sort with list
            # NOTE: this will be supplanted by query based method
            res = client.get(
                "/samples",
                query_string={
                    "ownerId": 1,
                    "orderBy": ["statusId", "param1", "param2", "id"],
                    "pageSize": 10,
                    "debug": False,
                },
                headers=self.headers,
            )
            Sample = self.Sample
            qry = (
                Sample.query.filter(Sample.owner_id == 1)
                .order_by(
                    Sample.status_id, Sample.param1, Sample.param2, Sample.id
                )
                .limit(10)
                .all()
            )

            self.assertEqual(res.status_code, 200)

            self.assertEqual(
                len(res.get_json()[Sample._class()]), len(qry),
            )

            self.assertListEqual(
                res.get_json()["Sample"], [item.to_dict() for item in qry],
            )

            # test debug
            res = client.get(
                "/samples",
                query_string={
                    "ownerId": 1,
                    "orderBy": ["statusId", "param1", "param2", "id"],
                    "pageSize": 10,
                    "debug": True,
                },
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 200)
            self.assertListEqual(
                res.get_json()["query"].split("\n"),
                [
                    "SELECT sample.id AS sample_id, sample.owner_id AS "
                    "sample_owner_id, sample.param1 AS sample_param1, "
                    "sample.param2 AS sample_param2, sample.status_id AS "
                    "sample_status_id ",
                    "FROM sample ",
                    "WHERE sample.owner_id = ? ORDER BY sample.status_id, "
                    "sample.param1, sample.param2, sample.id",
                    " LIMIT ? OFFSET ?",
                ],
            )

            # test max page size, default sort
            # NOTE: compare explicit queries
            res = client.get(
                "/samples1",
                query_string={"ownerId": 1, "pageSize": 10, "debug": False},
                headers=self.headers,
            )
            Sample = self.Sample
            qry = Sample.query.filter(Sample.owner_id == 1).limit(5).all()

            self.assertEqual(res.status_code, 200)

            self.assertEqual(
                len(res.get_json()[Sample._class()]), len(qry),
            )

            # offset
            # NOTE: compare explicit queries
            res = client.get(
                "/samples1",
                query_string={
                    "ownerId": 1,
                    "pageSize": 10,
                    "offset": 10,
                    "debug": False,
                },
                headers=self.headers,
            )
            Sample = self.Sample
            qry = (
                Sample.query.filter(Sample.owner_id == 1)
                .offset(10)
                .limit(5)
                .all()
            )

            self.assertEqual(res.status_code, 200)

            self.assertEqual(
                len(res.get_json()[Sample._class()]), len(qry),
            )

            # test variable in list -- first explicit axios list
            # needs to result in same SQLAlchemy query
            Sample = self.Sample
            qry = Sample.query.filter(
                Sample.status_id.in_([1, 2]), Sample.owner_id == 1
            ).all()
            target = [item.to_dict() for item in qry]

            qrys = [
                "statusId[]=1&statusId[]=2&owner_id=1&debug=false",
                "statusId=[1,2]&owner_id=1&debug=false",
                "statusId=1&statusId=2&owner_id=1&debug=potato",
                "statusId=1,2&owner_id=1&debug=false",
            ]

            for qry in qrys:
                with self.subTest(qry=qry):
                    res = client.get(
                        "/samples1", query_string=qry, headers=self.headers,
                    )
                    self.assertEqual(res.get_json()["Sample"], target)

                    self.assertEqual(res.status_code, 200)

    def test_internal_error(self):
        """
        With more error checking up front, this test
        will need to be redone.
        """
        db = self.db

        class Test550(db.Model):
            __tablename__ = "test550"
            id = db.Column(db.Integer, primary_key=True)

        db.create_all()

        Test550(id=300).save()

        class TestResource(CollectionModelResource):
            model_class = Test550
            serial_fields = ["faulty", "serial", "list"]

        self.api.add_resource(TestResource, "/tests")

        with self.app.test_client() as client:

            res = client.get("/tests", headers=self.headers,)

            self.assertDictEqual(
                res.get_json(),
                {"message": "Internal Server Error: method get: /tests"},
            )

    def test_process_get_input(self):

        db = self.db

        class Test1(db.Model):
            __tablename__ = "test1"
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String)

        db.create_all()

        class Test1Resource(CollectionModelResource):
            model_class = Test1

            def process_get_input(self, query, data):
                debug = data.get("debug")
                if debug == "False":
                    debug = False

                query = query.filter(self.model_class.name == "here we are")

                if debug:
                    return (True, (query, data))
                else:

                    if debug is None:
                        return (False, ({"message": "debug is None"}, 400))

                    return False, "debug is False"

        self.api.add_resource(Test1Resource, "/test1")

        with self.app.test_client() as client:
            res = client.get(
                "/test1", query_string={"debug": False}, headers=self.headers,
            )

            self.assertDictEqual(
                res.get_json(),
                {
                    "message": "malformed error in process_get_input: "
                    "debug is False"
                },
            )
            self.assertEqual(res.status_code, 500)

            # debug is None
            res = client.get("/test1", headers=self.headers)

            self.assertDictEqual(res.get_json(), {"message": "debug is None"})
            self.assertEqual(res.status_code, 400)

            # debug is True
            res = client.get(
                "/test1", query_string={"debug": True}, headers=self.headers,
            )

            self.assertListEqual(
                res.get_json()["query"].split("\n"),
                [
                    "SELECT test1.id AS test1_id, test1.name AS test1_name ",
                    "FROM test1 ",
                    "WHERE test1.name = ?",
                ],
            )
