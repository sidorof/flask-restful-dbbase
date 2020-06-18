.. code-block:: python

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


..
