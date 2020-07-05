# examples/post_only_resource.py
"""
This app provides an example of a resource with methods
limited to only POST. This describes a common registration process.

"""
# initialize
from datetime import date, datetime
from flask import Flask, request

from itsdangerous import URLSafeTimedSerializer

from flask_restful import Api, Resource
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import (
    ModelResource,
    MetaResource,
)
from flask_restful_dbbase.generator import create_resource


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "this is secret"
app.config['SECURITY_PASSWORD_SALT'] = "this is the salt"

api = Api(app)
db = DBBase(app)


# define users
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, nullable=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.WriteOnlyColumn(db.String(80), nullable=False)
    is_staff = db.Column(db.Boolean, default=False, nullable=True)
    is_active = db.Column(db.Boolean, default=False, nullable=True)
    is_account_current = db.Column(db.Boolean, default=False, nullable=True)

    date_joined = db.Column(db.Date, default=date.today, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)

    SERIAL_FIELDS = ["username", "email"]


db.create_all()

# tokens
def encode_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def decode_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return None
    return email


# before/after commits
def register_confirm(self, item, status_code):
    """
    This will be used in an after_commit function.
    It always receives an item and the default response status code.
    """

    try:
        # use the default status_code for response
        token = encode_token(item.email)
        print(f"The url /confirm/{token} would be included in the welcome email")
        return item, status_code
    except:
        # change the status code to something appropriate
        error = {"message": "Problem sending email"}
        return error, 400

def update_last_login(self, item, status_code):
    """
    This function runs in a before commit and updates the user
    record with the current date.
    """
    item.last_login = datetime.now()
    return item, status_code

# create register resource
RegisterResource = create_resource(
    name="RegisterResource",
    resource_class=ModelResource,
    model_class=User,
    methods=["post"],
    url_prefix="/",
    url_name="register",
    class_vars = {
        "after_commit": {
            "post": register_confirm
        }
    }
)

# ConfirmResource creation
class ConfirmResource(Resource):
    """
    This resource is best without ModelResource.

    * It uses the User model, but does not enforce the User.id
    to be part of the URL.
    * The confirm token is ephemeral, no need to save it.
    * It is easier to simply do the user query directly.
    * It does not need to return user information.
    """
    def get(self, **kwargs):
        token = kwargs.get("token", None)
        try:
            email = decode_token(token)
        except:
            msg = "Confirmation token has either expired or is invalid"
            return {"message": msg}, 401

        user = User.query.filter(User.email == email).first()

        if user is not None:

            user.is_active = True
            user.save()
            # front end would then redirect to sign-in
            return {"message": "Welcome to ________!"}, 200

        return {"message": "This email is not valid"}, 401


# create SignIn resource
SignInResource = create_resource(
    name="SignInResource",
    resource_class=ModelResource,
    model_class=User,
    methods=["post"],
    url_prefix="/",
    url_name="sign-in",
    class_vars={
        "before_commit": {"post": update_last_login}}
)

# meta resources
class RegisterMetaResource(MetaResource):
    resource_class = RegisterResource

class SignInMetaResource(MetaResource):
    resource_class = SignInResource

# add the resources
api.add_resource(RegisterResource, *RegisterResource.get_urls())
api.add_resource(SignInResource, *SignInResource.get_urls())
api.add_resource(ConfirmResource, '/confirm/<string:token>')

api.add_resource(RegisterMetaResource, *RegisterMetaResource.get_urls())
api.add_resource(SignInMetaResource, *SignInMetaResource.get_urls())


if __name__ == "__main__":
    app.run(debug=True)
