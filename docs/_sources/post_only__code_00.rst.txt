.. code-block:: python 

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
    
    
..