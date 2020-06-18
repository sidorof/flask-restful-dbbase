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
        """ small and generic """

        __tablename__ = "small_before"
        id = db.Column(db.Integer, nullable=True, primary_key=True)

    class SmallAfter(db.Model):
        """ small and generic """

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
                def process_get_input(self, qry, kwargs):
                    # assumes pretend decorator
                    # user_id = get_jwt_identity()

                    user_id = 1
                    qry = qry.filter_by(owner_id=user_id)
                    return True, qry

                def process_post_input(self, data):
                    # assumes pretend decorator
                    # user_id = get_jwt_identity()
                    user_id = 1

                    # see how owner is camel case, data at this stage
                    #   is not yet deserialized
                    if data.get("ownerId") == user_id:
                        return True, data

                    msg = "The user id does not match the owner id"
                    return (
                        False,
                        ({"message": msg}, 400)
                    )

                def process_put_input(self, qry, data, kwargs):
                    # assumes pretend decorator
                    # user_id = get_jwt_identity()
                    user_id = 1

                    # see how owner is camel case, data at this stage
                    #   is not yet deserialized
                    if data.get("ownerId") == user_id:
                        return True, (qry, data)

                    msg = "The user id does not match the owner id"
                    return (
                        False,
                        ({"message": msg}, 400)
                    )

                def process_patch_input(self, qry, data, kwargs):
                    # assumes pretend decorator
                    # user_id = get_jwt_identity()
                    user_id = 1

                    # see how owner is camel case, data at this stage
                    #   is not yet deserialized
                    if data.get("ownerId") == user_id:
                        return True, (qry, data)

                    return (
                        False,
                        ({"message": "The user id does not match the owner id"}, 400)
                    )

                def process_delete_input(self, qry, kwargs):
                    # assumes pretend decorator
                    # user_id = get_jwt_identity()
                    user_id = 1
                    qry = qry.filter_by(owner_id=user_id)
                    return True, qry

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
        cls.db.session.commit()
        cls.db.session.close()
        cls.Sample = None
        cls.OtherSample = None

        cls.db.drop_all()
        cls.db.Model.metadata.clear()
        cls.db = None
        del cls.db

    def test_get_with_input_processing(self):
        """ test_get_with_input_processing

        This pretends there is a method decorator for jwt. If it
        was only to know if the user is logged in, nothing extra is required.
        However, if a user only has access to a subset of recoords, then
        the `process_get_input` function can be used to determine whether the
        user is allowed for this specific record.

        """
        id = 1
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.get(f"/sample/{id}", headers=self.headers)
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {
                    "id": 1,
                    "ownerId": 1,
                    "param1": 1,
                    "param2": 2,
                    "statusId": 0,
                },
            )
            self.assertEqual(res.content_type, "application/json")

        # user is not an owner of this record
        id = 2
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.get(f"/sample/{id}", headers=self.headers)
            self.assertEqual(res.status_code, 404)
            self.assertDictEqual(
                res.get_json(), {"message": "Sample with id of 2 not found"},
            )
            self.assertEqual(res.content_type, "application/json")

    def test_post_with_input_processing(self):
        """ test_post_with_input_processing

        The input processing is similar to get, except that instead of
        the start of a query, data from the request is part of the function
        argument.

        self.process_post_input(data, kwargs)

        """
        sample = {"ownerId": 2, "param1": 5, "param2": 6}

        # mismatch owner id
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                f"/sample", data=json.dumps(sample), headers=self.headers
            )
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {"message": "The user id does not match the owner id"},
            )
            self.assertEqual(res.content_type, "application/json")

        # owner id and user id match
        sample = {"ownerId": 1, "param1": 5, "param2": 6}

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                f"/sample", data=json.dumps(sample), headers=self.headers
            )
            self.assertEqual(res.status_code, 201)

            # remove the id
            result = res.get_json()
            result.pop("id")
            self.assertDictEqual(
                result,
                {"ownerId": 1, "param1": 5, "param2": 6, "statusId": 0},
            )
            self.assertEqual(res.content_type, "application/json")

    def test_put_with_input_processing(self):
        """ test_put_with_input_processing

        The input processing in this case receives the start of a query,
        the data and kwargs.

        if the owner id matches the user id, and passes back the query and
        the data.

        Suppose that the input processing does something completely different
        here, and a specialized filter to the query is needed to complete?
        That is the reason that the query passes through the function.
        """
        sample = {"id": 1, "ownerId": 2, "param1": 5, "param2": 6}

        # mismatch owner id
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/sample/1", data=json.dumps(sample), headers=self.headers
            )
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {"message": "The user id does not match the owner id"}
            )
            self.assertEqual(res.content_type, "application/json")

        sample = {"id": 1, "ownerId": 1, "param1": 5, "param2": 6}

        # owner id matches user i
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/sample/1", data=json.dumps(sample), headers=self.headers
            )
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {
                    "id": 1,
                    "ownerId": 1,
                    "param1": 5,
                    "param2": 6,
                    "statusId": 0,
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_patch_with_input_processing(self):
        """ test_patch_with_input_processing

        The input processing in this case receives the start of a query,
        the data and kwargs.

        if the owner id matches the user id, and passes back the query and
        the data.

        Suppose that the input processing does something completely different
        here, and a specialized filter to the query is needed to complete?
        That is the reason that the query passes through the function.
        """
        sample = {"id": 1, "ownerId": 2, "param1": 5, "param2": 6}

        # mismatch owner id
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/sample/1", data=json.dumps(sample), headers=self.headers
            )
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(
                res.get_json(),
                {"message": "The user id does not match the owner id"},
            )
            self.assertEqual(res.content_type, "application/json")

        sample = {"id": 1, "ownerId": 1, "param1": 5, "param2": 6}

        # owner id matches user i
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/sample/1", data=json.dumps(sample), headers=self.headers
            )
            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {
                    "id": 1,
                    "ownerId": 1,
                    "param1": 5,
                    "param2": 6,
                    "statusId": 0,
                },
            )
            self.assertEqual(res.content_type, "application/json")

    def test_delete_with_input_processing(self):
        """ test_delete_with_input_processing

        The input processing in this case receives the start of a query,
        the data and kwargs.

        if the owner id matches the user id, and passes back the query and
        the data.

        Suppose that the input processing does something completely different
        here, and a specialized filter to the query is needed to complete?
        That is the reason that the query passes through the function.
        """
        # mismatch owner id
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.delete(f"/sample/100", headers=self.headers)

            self.assertEqual(res.status_code, 404)
            self.assertDictEqual(
                res.get_json(), {"message": "Sample with id of 100 not found"},
            )
            self.assertEqual(res.content_type, "application/json")

        # owner id matches user id
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.delete(f"/other-sample/1", headers=self.headers)

            self.assertEqual(res.status_code, 200)
            self.assertDictEqual(
                res.get_json(),
                {"message": "OtherSample with id of 1 is deleted"},
            )
            self.assertEqual(res.content_type, "application/json")


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
        return job, status_code


class GenericAdjustment(object):
    def __init__(self, *args, **kwargs):
        pass

    def run(self, resource_self, item, status_code):
        # change status code to teapot
        return item, 418


def generic_adjustment(resource_self, item, status_code):
    return item, 418


class TestModelBeforeAftertResource(unittest.TestCase):
    """ TestModelBeforeAftertResource

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
        cls.db.session.close()
        cls.Sample = None
        cls.OtherSample = None

        cls.db.drop_all()
        cls.db.Model.metadata.clear()
        cls.db = None
        del cls.db

    def test_post_start_job(self):
        """ test_post_start_job

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
                f"/ml-model", data=json.dumps(new_model), headers=self.headers
            )

            self.assertEqual(res.status_code, 202)

            # popping the start time, it will never match
            result = res.get_json()
            result.pop("startTime")
            self.assertDictEqual(
                res.get_json(),
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
        """ test_all_before_adjusts

        """
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                f"/small-before", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-before/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:

            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-before/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:

            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.delete(
                f"/small-before/{small.id}",
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
                f"/small-before", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-before/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:

            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-before/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:

            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.delete(
                f"/small-before/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

    def test_all_after_adjusts(self):
        """ test_all_after_adjusts

        """
        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()
            res = client.post(
                f"/small-after", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-after/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:

            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-after/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)

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
                f"/small-after", data=json.dumps({}), headers=self.headers
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:
            small = self.SmallBefore().save()
            if self.needs_setup:
                self.set_db()
            res = client.put(
                f"/small-after/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )
            self.assertEqual(res.status_code, 418)

        with self.app.test_client() as client:

            small = self.SmallBefore().save()

            if self.needs_setup:
                self.set_db()
            res = client.patch(
                f"/small-after/{small.id}",
                data=json.dumps(small.to_dict()),
                headers=self.headers,
            )

            self.assertEqual(res.status_code, 418)
