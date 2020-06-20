# tests/test_collection_model_resource.py
"""
This module tests collections.
"""
import unittest
from random import randint
import logging
import json
from datetime import datetime

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

            cls.api.add_resource(Sample1CollectionResource, "/sample1")
            cls.needs_setup = False

        headers = {"Content-Type": "application/json"}
        cls.set_db = set_db
        cls.app = app
        cls.api = api
        cls.db = db
        cls.headers = headers

    @classmethod
    def tearDownClass(cls):
        cls.db.session.commit()
        cls.db.session.close()
        cls.Sample = None

        cls.db.drop_all()
        cls.db.Model.metadata.clear()
        cls.db = None
        del cls.db

    def test_is_collection(self):
        class SampleCollection(CollectionModelResource):
            model_class = self.Sample

        self.assertTrue(SampleCollection.is_collection())

    def test_get_no_params(self):
        """ test_get_no_params

        """
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.get(f"/sample", headers=self.headers)

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
                f"/sample",
                query_string={
                    "ownerId": 1,
                    "orderby": "statusID",
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

            res = client.get(
                f"/sample",
                query_string={
                    "ownerId": 1,
                    "orderby": "statusID",
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
            # test max page size, default sort
            # NOTE: compare explicit queries
            res = client.get(
                f"/sample1",
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
                f"/sample1",
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
