# examples/owner_app_v2.py
"""
This app provides an example of modifying the processing flow
for the resource methods.

"""
# initialize
from functools import wraps
from datetime import date, datetime
from flask import Flask, request
from flask_restful import Api
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import (
    CollectionModelResource,
    ModelResource,
    MetaResource,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db = DBBase(app)


# define users
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, nullable=True, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.WriteOnlyColumn(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    is_staff = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    is_account_current = db.Column(db.Boolean, default=False, nullable=False)

    date_joined = db.Column(db.Date, default=date.today, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)


# define orders
class Order(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, nullable=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.String, nullable=False)
    ordered_at = db.Column(db.DateTime, default=datetime.now)
    status_id = db.Column(db.SmallInteger, default=0, nullable=True)

    jobs = db.relationship("Job", backref="order", lazy="immediate")


# define jobs
class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, nullable=True, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    started_at = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False
    )
    finished_at = db.Column(db.DateTime)
    status_id = db.Column(db.SmallInteger, default=0, nullable=True)


db.create_all()
# end database setup

# create users
user = User(
    username="our_main_user",
    password="verysecret",
    email="user_mainexample.com",
).save()


# mock authentication
def mock_jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = request.headers.get("Authorization", None)
        if user is not None and user.startswith("User"):
            # we're completely secure, sir
            return fn(*args, **kwargs)
        return {"message": "Unauthorized User"}, 401

    return wrapper


def get_identity():
    user = request.headers.get("Authorization", None)
    user_id = int(user.split(":")[1])
    return user_id


# create owner resources
class OwnerResource(ModelResource):
    """
    Pretend that jwt is being used for determining
    authenticated users.

    The basic strategy for process_{method}_input functions:

    Returns:
        status: (bool) : Success or failure
        data: (obj) :  if success, the data
                       if failure (explanation, status_code)

    That means the response.status_code can be tailored to fit your
    scenario.

    """

    method_decorators = [mock_jwt_required]

    def process_get_input(self, query, data, kwargs):
        """
        This function runs in the GET method with access to
        the Model.query object.
        """
        user_id = get_identity()
        if user_id:
            query = query.filter_by(owner_id=user_id)
            return True, (query, data)

        return False, ({"message": "Not found"}, 404)

    def process_post_input(self, data):
        """
        This function runs in the POST method with access to
        the data included with the request.
        """
        user_id = get_identity()
        owner_id = data.get("ownerId", None)
        if owner_id:
            if int(owner_id) == user_id:
                return True, data

        return (
            False,
            ({"message": "The user id does not match the owner id"}, 400),
        )

    def process_put_input(self, query, data, kwargs):
        """
        This function runs in the PUT method with access to
        the data included with the request.
        """
        user_id = get_identity()
        owner_id = data.get("ownerId", None)
        if owner_id:
            if int(owner_id) == user_id:
                return True, (query, data)

        return (
            False,
            ({"message": "The user id does not match the owner id"}, 400),
        )

    def process_patch_input(self, query, data, kwargs):
        """
        This function runs in the PATCH method with access to
        the data included with the request.
        """
        user_id = get_identity()
        owner_id = data.get("ownerId", None)
        if owner_id:
            if int(owner_id) == user_id:
                return True, data

        return (
            False,
            ({"message": "The user id does not match the owner id"}, 400),
        )

    def process_delete_input(self, query, kwargs):
        """
        This function runs in the DELETE method.
        """
        user_id = get_identity()
        if user_id:
            query = query.filter_by(owner_id=user_id)
            return True, query

        return False, ("Not found", 404)


class OwnerCollectionResource(CollectionModelResource):
    """
    Pretend that jwt is being used for determine authenticated users.
    """

    method_decorators = [mock_jwt_required]

    def process_get_input(self, query, data):
        user_id = get_identity()
        if user_id:
            query = query.filter_by(owner_id=user_id)
            return True, (query, data)

        return False, ("The user id is not authorized", 400)


# order resources
class OrderCollection(OwnerCollectionResource):
    model_class = Order
    url_prefix = "/api/v2"


# create job
def create_job(self, order, status_code):
    """
    This function creates a processing job from an order.

    It runs after the order is saved to the database, then
    creates a job and submits it to processing.

    Args:
        order: (obj) : The order that is to be processed.
        status_code: (int) :
    Returns:
        return_status: (bool) : True to coninue,
            False  to return just a message
        job: (obj) : The job that is created.
        status_code: (int) : The new response status
        code.
    """

    job = Job(owner_id=order.owner_id, order_id=order.id).save()
    status_code = 202
    # this is where you send the job to queue

    return True, job, status_code


# new order resource
class OrderResource(OwnerResource):
    model_class = Order
    url_prefix = "/api/v2"

    serial_fields = {
        "post": {Job: ["id", "started_at", "status_id"]},
        "put": {Job: ["id", "started_at", "status_id"]},
    }

    after_commit = {"post": create_job, "put": create_job}


# remaining other resources
class OrderMetaCollection(MetaResource):
    resource_class = OrderCollection


class OrderMeta(MetaResource):
    resource_class = OrderResource


# job resources
class JobCollection(OwnerCollectionResource):
    model_class = Job
    url_prefix = "/api/v2"


class JobResource(OwnerResource):
    model_class = Job
    url_prefix = "/api/v2"


class JobMetaCollection(MetaResource):
    resource_class = JobCollection


class JobMeta(MetaResource):
    resource_class = JobResource


# add the resources to the API
api.add_resource(OrderCollection, *OrderCollection.get_urls())
api.add_resource(OrderResource, *OrderResource.get_urls())
api.add_resource(OrderMetaCollection, *OrderMetaCollection.get_urls())
api.add_resource(OrderMeta, *OrderMeta.get_urls())

api.add_resource(JobCollection, *JobCollection.get_urls())
api.add_resource(JobResource, *JobResource.get_urls())
api.add_resource(JobMetaCollection, *JobMetaCollection.get_urls())
api.add_resource(JobMeta, *JobMeta.get_urls())

if __name__ == "__main__":
    app.run(debug=True)
