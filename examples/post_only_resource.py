# examples/post_only_resource.py
"""
This app provides an example of a resource with methods
limited to only POST.
"""
# initialize
from flask import Flask
from flask_restful import Api
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import ModelResource
from flask_restful_dbbase.generator import create_resource


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app)
db = DBBase(app)


# define table
class AModel(db.Model):
    __tablename__ = "amodel"

    id = db.Column(db.Integer, nullable=True, primary_key=True)
    description = db.Column(db.String(80), unique=True, nullable=False)
    num_variable = db.Column(db.Integer, nullable=False)


db.create_all()


# before/after commits
def after_commit(self, item, status_code):
    """
    This will be used in an after_commit function.

    In this case, the process is diverted to a
    message, new status code and the method exits with
    this message.
    """
    # processing takes place here
    payload = {
        "message": "This is no longer a REST resource. We can do anything.",
        "data": item.to_dict(),
    }

    return False, payload, 419


# create a post-only resource
PostOnlyResource = create_resource(
    name="PostOnlyResource",
    resource_class=ModelResource,
    model_class=AModel,
    methods=["post"],
    url_prefix="/",
    url_name="a-model-command",
    class_vars={"after_commit": {"post": after_commit},},
)

# add the resources
api.add_resource(PostOnlyResource, *PostOnlyResource.get_urls())


if __name__ == "__main__":
    app.run(debug=True)
