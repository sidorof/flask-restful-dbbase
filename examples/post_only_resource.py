# examples/post_only_resource.py
"""
This app provides an example of a resource with methods
limited to only POST.
"""
# initialize
from datetime import date
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


db.create_all()


# create a register resource
class RegisterResource(ModelResource):
    model_class = User
    only_methods = ["post"]
    url_prefix = "/api/v1"
    url_name = "register"

    #   dates in string form -- such as Sqlite3
    use_date_conversions = True


# the rest of the resources
class RegisterMetaResource(MetaResource):
    resource_class = RegisterResource


# add the resources to the API
api.add_resource(RegisterResource, *RegisterResource.get_urls())
api.add_resource(RegisterMetaResource, *RegisterMetaResource.get_urls())

print()
print(dir(RegisterResource))
print()

print("urls:")
print(*RegisterResource.get_urls())
print(*RegisterMetaResource.get_urls())

if __name__ == "__main__":
    app.run(debug=True)
