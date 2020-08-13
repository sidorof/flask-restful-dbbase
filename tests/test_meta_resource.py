# tests/test_meta_resource.py
import unittest
import flask
import flask_restful
from flask_restful_dbbase import DBBase
from flask_restful_dbbase.resources import (
    ModelResource,
    CollectionModelResource,
    MetaResource,
)


def create_models(db):
    """create a sample models"""

    class Product(db.Model):
        __tablename__ = "product"

        id = db.Column(db.Integer, nullable=True, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        description = db.Column(db.String(200), nullable=False)
        vendor_id = db.Column(db.Integer, nullable=False)
        vendor_part_number = db.Column(db.String, nullable=False)
        last_ordered = db.Column(db.DateTime, nullable=True)
        active = db.Column(db.SmallInteger, default=False, nullable=True)

    db.create_all()

    return Product


class TestMetaModelResource(unittest.TestCase):
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
            Product = create_models(db)
            cls.Product = Product

            class ProductResource(ModelResource):
                model_class = cls.Product

            class ProductCollection(CollectionModelResource):
                model_class = cls.Product

            # alternate resource classes
            class ProductResource1(ModelResource):
                model_class = cls.Product
                url_prefix = "/api/v1"

            class ProductCollection1(CollectionModelResource):
                model_class = cls.Product
                url_prefix = "/api/v1"

            class ProductMetaResource(MetaResource):
                resource_class = ProductResource

            class ProductMetaCollection(MetaResource):
                resource_class = ProductCollection

            # alternate meta resource classes
            class ProductMetaResource1(MetaResource):
                resource_class = ProductResource1

            class ProductMetaCollection1(MetaResource):
                resource_class = ProductCollection1

            cls.api.add_resource(ProductResource, *ProductResource.get_urls())
            cls.api.add_resource(
                ProductMetaResource, *ProductMetaResource.get_urls()
            )

            cls.api.add_resource(
                ProductMetaCollection, *ProductMetaCollection.get_urls()
            )

            cls.api.add_resource(
                ProductResource1, *ProductResource1.get_urls()
            )
            cls.api.add_resource(
                ProductMetaResource1, *ProductMetaResource1.get_urls()
            )

            cls.api.add_resource(
                ProductMetaCollection1, *ProductMetaCollection1.get_urls()
            )

            cls.ProductResource = ProductResource
            cls.ProductMetaResource = ProductMetaResource
            cls.ProductMetaCollection = ProductMetaCollection

            cls.ProductResource1 = ProductResource1
            cls.ProductMetaResource1 = ProductMetaResource1
            cls.ProductMetaCollection1 = ProductMetaCollection1

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

    def test_default_class_variables(self):

        self.assertIsNone(MetaResource.resource_class)
        self.assertEqual(MetaResource.url_prefix, "meta")
        self.assertIsNone(MetaResource.url_name)

    def test_get_urls(self):
        self.assertListEqual(
            self.ProductMetaResource.get_urls(), ["/meta/products/single"]
        )

        self.assertListEqual(
            self.ProductMetaCollection.get_urls(),
            ["/meta/products/collection"],
        )

        # with specified path
        self.ProductMetaResource.url_prefix = "api/v2"
        self.ProductMetaResource.url_name = "different"

        self.assertListEqual(
            self.ProductMetaResource.get_urls(), ["/api/v2/different"]
        )

        self.assertListEqual(
            self.ProductMetaResource1.get_urls(),
            ["/api/v1/meta/products/single"],
        )

        self.assertListEqual(
            self.ProductMetaCollection1.get_urls(),
            ["/api/v1/meta/products/collection"],
        )

    def test_get(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get("/meta/products/single", headers=self.headers)

            self.assertEqual(res.status_code, 200)

            self.assertDictEqual(
                res.get_json(),
                {
                    "modelClass": "Product",
                    "urlPrefix": "/",
                    "baseUrl": "/products",
                    "methods": {
                        "get": {
                            "url": "/products/<int:id>",
                            "input": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                }
                            },
                            "responses": [
                                {
                                    "fields": {
                                        "name": {
                                            "type": "string",
                                            "maxLength": 50,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "lastOrdered": {
                                            "type": "date-time",
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "vendorPartNumber": {
                                            "type": "string",
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "description": {
                                            "type": "string",
                                            "maxLength": 200,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "id": {
                                            "type": "integer",
                                            "format": "int32",
                                            "primary_key": True,
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "active": {
                                            "type": "integer",
                                            "format": "int8",
                                            "nullable": True,
                                            "default": {
                                                "for_update": False,
                                                "arg": False,
                                            },
                                            "info": {},
                                        },
                                        "vendorId": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": False,
                                            "info": {},
                                        },
                                    }
                                }
                            ],
                        },
                        "post": {
                            "url": "/products",
                            "input": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "name": {
                                    "type": "string",
                                    "maxLength": 50,
                                    "nullable": False,
                                    "info": {},
                                },
                                "description": {
                                    "type": "string",
                                    "maxLength": 200,
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendorId": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendorPartNumber": {
                                    "type": "string",
                                    "nullable": False,
                                    "info": {},
                                },
                                "lastOrdered": {
                                    "type": "date-time",
                                    "nullable": True,
                                    "info": {},
                                },
                                "active": {
                                    "type": "integer",
                                    "format": "int8",
                                    "nullable": True,
                                    "default": {
                                        "for_update": False,
                                        "arg": False,
                                    },
                                    "info": {},
                                },
                            },
                            "responses": [
                                {
                                    "fields": {
                                        "name": {
                                            "type": "string",
                                            "maxLength": 50,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "lastOrdered": {
                                            "type": "date-time",
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "vendorPartNumber": {
                                            "type": "string",
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "description": {
                                            "type": "string",
                                            "maxLength": 200,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "id": {
                                            "type": "integer",
                                            "format": "int32",
                                            "primary_key": True,
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "active": {
                                            "type": "integer",
                                            "format": "int8",
                                            "nullable": True,
                                            "default": {
                                                "for_update": False,
                                                "arg": False,
                                            },
                                            "info": {},
                                        },
                                        "vendorId": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": False,
                                            "info": {},
                                        },
                                    }
                                }
                            ],
                        },
                        "put": {
                            "url": "/products/<int:id>",
                            "input": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "name": {
                                    "type": "string",
                                    "maxLength": 50,
                                    "nullable": False,
                                    "info": {},
                                },
                                "description": {
                                    "type": "string",
                                    "maxLength": 200,
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendorId": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendorPartNumber": {
                                    "type": "string",
                                    "nullable": False,
                                    "info": {},
                                },
                                "lastOrdered": {
                                    "type": "date-time",
                                    "nullable": True,
                                    "info": {},
                                },
                                "active": {
                                    "type": "integer",
                                    "format": "int8",
                                    "nullable": True,
                                    "default": {
                                        "for_update": False,
                                        "arg": False,
                                    },
                                    "info": {},
                                },
                            },
                            "responses": [
                                {
                                    "fields": {
                                        "name": {
                                            "type": "string",
                                            "maxLength": 50,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "lastOrdered": {
                                            "type": "date-time",
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "vendorPartNumber": {
                                            "type": "string",
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "description": {
                                            "type": "string",
                                            "maxLength": 200,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "id": {
                                            "type": "integer",
                                            "format": "int32",
                                            "primary_key": True,
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "active": {
                                            "type": "integer",
                                            "format": "int8",
                                            "nullable": True,
                                            "default": {
                                                "for_update": False,
                                                "arg": False,
                                            },
                                            "info": {},
                                        },
                                        "vendorId": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": False,
                                            "info": {},
                                        },
                                    }
                                }
                            ],
                        },
                        "patch": {
                            "url": "/products/<int:id>",
                            "input": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "name": {
                                    "type": "string",
                                    "maxLength": 50,
                                    "nullable": False,
                                    "info": {},
                                },
                                "description": {
                                    "type": "string",
                                    "maxLength": 200,
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendorId": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendorPartNumber": {
                                    "type": "string",
                                    "nullable": False,
                                    "info": {},
                                },
                                "lastOrdered": {
                                    "type": "date-time",
                                    "nullable": True,
                                    "info": {},
                                },
                                "active": {
                                    "type": "integer",
                                    "format": "int8",
                                    "nullable": True,
                                    "default": {
                                        "for_update": False,
                                        "arg": False,
                                    },
                                    "info": {},
                                },
                            },
                            "responses": [
                                {
                                    "fields": {
                                        "name": {
                                            "type": "string",
                                            "maxLength": 50,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "lastOrdered": {
                                            "type": "date-time",
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "vendorPartNumber": {
                                            "type": "string",
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "description": {
                                            "type": "string",
                                            "maxLength": 200,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "id": {
                                            "type": "integer",
                                            "format": "int32",
                                            "primary_key": True,
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "active": {
                                            "type": "integer",
                                            "format": "int8",
                                            "nullable": True,
                                            "default": {
                                                "for_update": False,
                                                "arg": False,
                                            },
                                            "info": {},
                                        },
                                        "vendorId": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": False,
                                            "info": {},
                                        },
                                    }
                                }
                            ],
                        },
                        "delete": {
                            "url": "/products/<int:id>",
                            "input": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                }
                            },
                            "responses": [{}],
                        },
                    },
                    "table": {
                        "Product": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "name": {
                                    "type": "string",
                                    "maxLength": 50,
                                    "nullable": False,
                                    "info": {},
                                },
                                "description": {
                                    "type": "string",
                                    "maxLength": 200,
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendor_id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendor_part_number": {
                                    "type": "string",
                                    "nullable": False,
                                    "info": {},
                                },
                                "last_ordered": {
                                    "type": "date-time",
                                    "nullable": True,
                                    "info": {},
                                },
                                "active": {
                                    "type": "integer",
                                    "format": "int8",
                                    "nullable": True,
                                    "default": {
                                        "for_update": False,
                                        "arg": False,
                                    },
                                    "info": {},
                                },
                            },
                            "xml": "Product",
                        }
                    },
                },
            )

    def test_get_with_method(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/meta/products/single?method=get", headers=self.headers
            )
            self.assertEqual(res.status_code, 200)

            self.assertDictEqual(
                res.get_json(),
                {
                    "modelClass": "Product",
                    "urlPrefix": "/",
                    "baseUrl": "/products",
                    "methods": {
                        "get": {
                            "url": "/products/<int:id>",
                            "input": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                }
                            },
                            "responses": [
                                {
                                    "fields": {
                                        "id": {
                                            "type": "integer",
                                            "format": "int32",
                                            "primary_key": True,
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "name": {
                                            "type": "string",
                                            "maxLength": 50,
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "active": {
                                            "type": "integer",
                                            "format": "int8",
                                            "nullable": True,
                                            "default": {
                                                "for_update": False,
                                                "arg": False,
                                            },
                                            "info": {},
                                        },
                                        "lastOrdered": {
                                            "type": "date-time",
                                            "nullable": True,
                                            "info": {},
                                        },
                                        "vendorId": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "vendorPartNumber": {
                                            "type": "string",
                                            "nullable": False,
                                            "info": {},
                                        },
                                        "description": {
                                            "type": "string",
                                            "maxLength": 200,
                                            "nullable": False,
                                            "info": {},
                                        },
                                    }
                                }
                            ],
                        }
                    },
                    "table": {
                        "Product": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": True,
                                    "nullable": True,
                                    "info": {},
                                },
                                "name": {
                                    "type": "string",
                                    "maxLength": 50,
                                    "nullable": False,
                                    "info": {},
                                },
                                "description": {
                                    "type": "string",
                                    "maxLength": 200,
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendor_id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": False,
                                    "info": {},
                                },
                                "vendor_part_number": {
                                    "type": "string",
                                    "nullable": False,
                                    "info": {},
                                },
                                "last_ordered": {
                                    "type": "date-time",
                                    "nullable": True,
                                    "info": {},
                                },
                                "active": {
                                    "type": "integer",
                                    "format": "int8",
                                    "nullable": True,
                                    "default": {
                                        "for_update": False,
                                        "arg": False,
                                    },
                                    "info": {},
                                },
                            },
                            "xml": "Product",
                        }
                    },
                },
            )

    def test_get_with_bad_method(self):

        with self.app.test_client() as client:
            if self.needs_setup:
                self.set_db()

            res = client.get(
                "/meta/products/single?method=bad", headers=self.headers
            )

            self.assertEqual(res.status_code, 400)

            self.assertDictEqual(
                res.get_json(),
                {"message": "Method 'bad' is not found for this resource"},
            )
