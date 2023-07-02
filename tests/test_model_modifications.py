# tests/test_model_modifications.py
"""
This module tests ways to use the sample resources beyond the
basic REST functionality.

Tests
* linkage with permission decorators : such decorators can be connected
with the methods to limit or filter access to the database such as by owner
or staff.

* before_commit : Prior to a save/delete can make adjustments to a
record as necessary..

* after_commit : After saving, a function can be run, by method, that could
possiby do such things as initiate a job and return the job particulars in
place of the original sample.

"""
import unittest
import logging
import json
from datetime import datetime

import flask
import flask_restful
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import ModelResource


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

    class OtherSample(db.Model):
        __tablename__ = "other_sample"
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        owner_id = db.Column(db.Integer, nullable=False)

    db.create_all()

    # sample data
    Sample(owner_id=1, param1=1, param2=2).save()
    Sample(owner_id=2, param1=3, param2=4).save()
    Sample(id=100, owner_id=2, param1=5, param2=6).save()
    Sample(id=101, owner_id=2, param1=5, param2=6).save()
    Sample(id=102, owner_id=2, param1=5, param2=6).save()
    Sample(id=103, owner_id=2, param1=5, param2=6).save()
    Sample(id=104, owner_id=2, param1=5, param2=6).save()

    OtherSample(owner_id=1).save()

    return Sample, OtherSample


def create_models(db):
    """
    create models that have permissions on owner_id
    """

    class MlModel(db.Model):
        __tablename__ = "ml_model"
        id = db.Column(db.Integer, nullable=True, primary_key=True)
        owner_id = db.Column(db.Integer, nullable=False)
        param1 = db.Column(db.Integer, nullable=False)
        param2 = db.Column(db.Integer, nullable=False)
        result = db.Column(db.Float, nullable=True)
        status_id = db.Column(db.SmallInteger, default=0, nullable=True)

    class Job(db.Model):
        __tablename__ = "job"

        id = db.Column(db.Integer, nullable=True, primary_key=True)

        # NOTE: change to this to False in integration
        #       add relation here
        owner_id = db.Column(db.Integer, nullable=False)
        model_id = db.Column(db.Integer, nullable=False)
        start_time = db.Column(
            db.DateTime, default=datetime.now, nullable=False
        )
        end_time = db.Column(db.DateTime)
        job_type_id = db.Column(db.Integer, nullable=False)
        status_id = db.Column(db.SmallInteger, default=0, nullable=True)

    class SmallBefore(db.Model):
        """small and generic"""

        __tablename__ = "small_before"
        id = db.Column(db.Integer, nullable=True, primary_key=True)

    class SmallAfter(db.Model):
        """small and generic"""

        __tablename__ = "small_after"
        id = db.Column(db.Integer, nullable=True, primary_key=True)

    db.create_all()

    return MlModel, Job, SmallBefore, SmallAfter


class TestModelProcResource(unittest.TestCase):
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
            Sample, OtherSample = create_samples(db)
            cls.Sample = Sample
            cls.OtherSample = OtherSample

            class OtherSampleResource(ModelResource):
                model_class = cls.OtherSample

            class SampleResource(ModelResource):
                model_class = cls.Sample
                method_decorators = [
                    # pretend_jwt_required
                ]

                # some test process input functions
                def process_get_input(self, qry, data, kwargs):
                    """Returns True/False, depending on status."""

                    # use explicit variables to make it easier to validate
                    if "set_status" in data:
                        status = data.pop("set_status")[0]
                        if status == "good True status":
                            return {"status": True, "query": qry, "data": data}
                        elif status == "bad True status":
                            return {"status": True}

                        elif status == "good False status":
                            return {
                                "status": False,
                                "message": status,
                                "status_code": 400,
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

                def process_post_input(self, data):
                    """Returns True/False, depending on status."""

                    # use explicit variables to make it easier to validate
                    if "set_status" in data:
                        status = data.pop("set_status")
                        if status == "good True status":
                            return {"status": True, "data": data}
                        elif status == "bad True status":
                            return {"status": True}

                        elif status == "good False status":
                            return {
                                "status": False,
                                "message": status,
                                "status_code": 400,
                            }
                        elif status == "bad False Status":
                            return {
                                "status": False,
                                "message": status,
                            }
                        else:
                            # missing status
                            return "something else"

                    return {"status": True, "data": data}

                def process_put_input(self, qry, data, kwargs):
                    """Returns True/False, depending on status."""

                    # use explicit variables to make it easier to validate
                    if "set_status" in data:
                        status = data.pop("set_status")
                        if status == "good True status":
                            return {"status": True, "query": qry, "data": data}
                        elif status == "bad True Status":
                            return {"status": True}

                        elif status == "good False status":
                            return {
                                "status": False,
                                "message": status,
                                "status_code": 400,
                            }
                        elif status == "bad False Status":
                            return {
                                "status": False,
                                "message": status,
                            }
                        else:
                            # missing status
                            return "something else"

                    return {"status": True, "query": qry, "data": data}

                def process_patch_input(self, qry, data, kwargs):
                    """Returns True/False, depending on status."""

                    # use explicit variables to make it easier to validate
                    if "set_status" in data:
                        status = data.pop("set_status")
                        if status == "good True status":
                            return {"status": True, "query": qry, "data": data}
                        elif status == "bad True Status":
                            return {"status": True}

                        elif status == "good False status":
                            return {
                                "status": False,
                                "message": status,
                                "status_code": 400,
                            }
                        elif status == "bad False Status":
                            return {
                                "status": False,
                                "message": status,
                            }
                        else:
                            # missing status
                            return "something else"

                    return {"status": True, "query": qry, "data": data}

            # Delete testing is separate because it is easier
            # to have a separate process_delete_input for each scenario.
            # 1.  Status: good True, => Query
            # 2.  Status: bad True, => 500
            # 3.  Status: bad False, => 500
            # 4.  Status: good False, => 400
            class DeleteResource1(ModelResource):
                model_class = cls.Sample

                def process_delete_input(self, qry, kwargs):
                    return {"status": True, "query": qry}

            cls.api.add_resource(DeleteResource1, "/delete1/<int:id>")

            class DeleteResource2(ModelResource):
                model_class = cls.Sample

                def process_delete_input(self, qry, kwargs):
                    # missing query
                    return {"status": True}

            cls.api.add_resource(DeleteResource2, "/delete2/<int:id>")

            class DeleteResource3(ModelResource):
                model_class = cls.Sample

                def process_delete_input(self, qry, kwargs):
                    # missing status_code
                    return {"status": False, "message": "This is a test"}

            cls.api.add_resource(DeleteResource3, "/delete3/<int:id>")

            class DeleteResource4(ModelResource):
                model_class = cls.Sample

                def process_delete_input(self, qry, kwargs):
                    return {
                        "status": False,
                        "message": "Test",
                        "status_code": 400,
                    }

            cls.api.add_resource(DeleteResource4, "/delete4/<int:id>")

            cls.api.add_resource(
                OtherSampleResource, *OtherSampleResource.get_urls()
            )
            cls.api.add_resource(SampleResource, *SampleResource.get_urls())
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
        cls.db.drop_all()
        cls.db.Model.metadata.clear()
        cls.db = None
        del cls.db

    def test_get_with_input_processing(self):
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples/1",
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
                "/samples/1",
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
                "/samples/1",
                query_string={"set_status": "good False status"},
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 400)

        # # False, without correct message format
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/samples/1",
                query_string={"set_status": "bad False status"},
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)

    def test_post_with_input_processing(self):
        """test_post_with_input_processing"""

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "bad True status",
            }

            res = client.post(
                "/samples",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)
        #
        # # True, good with correct tuple
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "good True status",
            }
            res = client.post(
                "/samples",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 201)

        # # False, good with correct tuple
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "good False status",
            }
            res = client.post(
                "/samples",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 400)

        # # False, without correct message format
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "bad False status",
            }

            res = client.post(
                "/samples",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)

    def test_put_with_input_processing(self):
        """test_put_with_input_processing"""

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "bad True status",
            }

            res = client.put(
                "/samples/1",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)
        # True, good with correct tuple
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "good True status",
            }
            res = client.put(
                "/samples/1",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 200)

        # False, good with correct tuple
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "good False status",
            }
            res = client.put(
                "/samples/1",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 400)

        # False, without correct message format
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "bad False status",
            }

            res = client.put(
                "/samples/1",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)

    def test_patch_with_input_processing(self):
        """test_patch_with_input_processing"""

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "bad True status",
            }

            res = client.patch(
                "/samples/1",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)
        # True, good with correct tuple
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "good True status",
            }
            res = client.patch(
                "/samples/1",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 200)

        # False, good with correct tuple
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "good False status",
            }
            res = client.patch(
                "/samples/1",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 400)

        # False, without correct message format
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            sample = {
                "ownerId": 2,
                "param1": 5,
                "param2": 6,
                "set_status": "bad False status",
            }

            res = client.patch(
                "/samples/1",
                data=json.dumps(sample),
                headers=self.headers,
            )

            res_qry = res.json
            self.assertEqual(res.status_code, 500)

    def test_delete_with_input_processing(self):
        """test_delete_with_input_processing"""

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.delete("/delete1/101", headers=self.headers)

            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {"message": "Sample with {'id': 101} is deleted"},
            )
            self.assertEqual(res.content_type, "application/json")

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.delete("/delete2/102", headers=self.headers)

            self.assertEqual(res.status_code, 500)

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.delete("/delete3/103", headers=self.headers)

            self.assertEqual(res.status_code, 500)
            self.assertEqual(res.content_type, "application/json")

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.delete("/delete4/104", headers=self.headers)

            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {"message": "Test"},
            )


class JobCreator(object):
    def __init__(self, class_name):
        self.Job = class_name

    def run(self, resource_self, item, status_code):
        # obj_self gives access resource characteristics
        # but not used in this case
        data = item.to_dict(to_camel_case=False)
        job = self.Job()
        job = self.Job(
            owner_id=data["owner_id"],
            model_id=data["id"],
            job_type_id=0,
            status_id=0,
        ).save()
        if resource_self.serial_fields is None:
            resource_self.serial_fields = {}
        resource_self.serial_fields["post"] = self.Job.get_serial_fields()

        # job submitted here ->

        status_code = 202
        return True, job, status_code


class GenericAdjustment(object):
    def __init__(self, *args, **kwargs):
        pass

    def run(self, resource_self, item, status_code):
        # change status code to teapot
        return True, item, 418


def generic_adjustment(resource_self, item, status_code):
    return True, item, 418


def generic_diversion(resource_self, item, status_code):
    return False, {"message": "something else"}, 418


class TestModelBeforeAftertResource(unittest.TestCase):
    """TestModelBeforeAftertResource

    This class tests creating a sample, submitting it to a queue
    as a job, returning the job particulars instead.
    """

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
            MlModel, Job, SmallBefore, SmallAfter = create_models(db)
            cls.MlModel = MlModel
            cls.Job = Job
            cls.SmallBefore = SmallBefore
            cls.SmallAfter = SmallAfter

            class Job(ModelResource):
                model_class = cls.Job

            class MlModel(ModelResource):
                model_class = cls.MlModel
                after_commit = {"post": JobCreator(class_name=cls.Job)}

            cls.api.add_resource(Job, *Job.get_urls())
            cls.api.add_resource(MlModel, *MlModel.get_urls())

            class SmallBefore(ModelResource):
                model_class = cls.SmallBefore
                before_commit = {
                    "post": generic_adjustment,
                    "put": generic_adjustment,
                    "patch": generic_adjustment,
                    "delete": generic_adjustment,
                }

            class SmallAfter(ModelResource):
                model_class = cls.SmallAfter
                after_commit = {
                    "post": generic_adjustment,
                    "put": generic_adjustment,
                    "patch": generic_adjustment,
                }

            cls.api.add_resource(SmallBefore, *SmallBefore.get_urls())
            cls.api.add_resource(SmallAfter, *SmallAfter.get_urls())

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
        cls.db.session.remove()
        cls.db.drop_all()
        cls.db.Model.metadata.clear()
        cls.db = None
        del cls.db

    def test_post_start_job(self):
        """test_post_start_job

        The input processing is similar to get, except that instead of
        the start of a query, data from the request is part of the function
        argument.

        self.process_post_input(data, kwargs)

        """
        new_model = {"ownerId": 2, "param1": 5, "param2": 6}

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                "/ml-models", data=json.dumps(new_model), headers=self.headers
            )

            self.assertEqual(res.status_code, 202)

            # popping the start time, it will never match
            result = res.get_json()
            result.pop("startTime")
            self.assertDictEqual(
                result,
                {
                    "id": 1,
                    "ownerId": 2,
                    "modelId": 1,
                    "statusId": 0,
                    "jobTypeId": 0,
                    "endTime": None,
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_all_before_adjusts(self):
        """test_all_before_adjusts"""
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                "/small-befores", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.delete(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

        # switch to class based adjustments
        a = self.app.view_functions["smallbefore"]
        a.view_class.before_commit = {
            "post": GenericAdjustment(),
            "put": GenericAdjustment(),
            "patch": GenericAdjustment(),
            "delete": GenericAdjustment(),
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                "/small-befores", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.delete(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

        # switch to exit version adjustments
        a = self.app.view_functions["smallbefore"]
        a.view_class.before_commit = {
            "post": generic_diversion,
            "put": generic_diversion,
            "patch": generic_diversion,
            "delete": generic_diversion,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                "/small-befores", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)
            self.assertDictEqual(res.get_json(), {"message": "something else"})

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)
            self.assertDictEqual(res.get_json(), {"message": "something else"})

        with self.app.test_client() as client:
            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)
            self.assertDictEqual(res.get_json(), {"message": "something else"})

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.delete(
                f"/small-befores/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)
            self.assertDictEqual(res.get_json(), {"message": "something else"})

    def test_all_after_adjusts(self):
        """test_all_after_adjusts"""
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                "/small-afters", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-afters/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-afters/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

        # switch to diversions
        a = self.app.view_functions["smallafter"]
        a.view_class.after_commit = {
            "post": generic_diversion,
            "put": generic_diversion,
            "patch": generic_diversion,
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                "/small-afters", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)
            self.assertDictEqual(res.get_json(), {"message": "something else"})

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-afters/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)
            self.assertDictEqual(res.get_json(), {"message": "something else"})

        with self.app.test_client() as client:
            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-afters/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)
            self.assertDictEqual(res.get_json(), {"message": "something else"})

        # switch to class based adjustments
        a = self.app.view_functions["smallafter"]
        a.view_class.after_commit = {
            "post": GenericAdjustment(),
            "put": GenericAdjustment(),
            "patch": GenericAdjustment(),
        }

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                "/small-afters", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-afters/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-afters/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)
