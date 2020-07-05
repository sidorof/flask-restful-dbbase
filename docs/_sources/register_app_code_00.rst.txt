.. code-block:: python 

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
    
    
..