==========
User Guide
==========

**Flask-Restful-Extended** builds on the excellent work of Flask-Restful by implementing a version Resources that can act as hierarchical nodes.
------------
Introduction
------------

-------------
A Minimal API
-------------

A minimal Flask-RESTful-Extended API looks like this:


.. code-block:: python

    from flask import Flask
    from flask_restful_extended import NodeResource, Api

    app = Flask(__name__)
    api = Api(app)

    root_resource = NodeResource(url='/api)
    version_resource = NodeResource(url='v1').set_parent(root_resource)



    api.add_resource(HelloWorld, '/')

    if __name__ == '__main__':
        app.run(debug=True)

..
