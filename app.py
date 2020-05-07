# app.py
from flask import Flask
from flask_restful import Api
#from flask_restful_extended import NodeResource
from extended import NodeResource

app = Flask(__name__)
api = Api(app)

root_resource = NodeResource(url='/api')
#version_resource = NodeResource(url='v1').set_parent(root_resource)

# /api/v1/parents/<int:id>/children

class ParentsResource(NodeResource):

    url_prefix = 'parents'
    def get(self, id: int):

        return id

class ChildrenResource(NodeResource):

    url_prefix = 'children'
    def get(self, id: int):

        return id

#ParentsResource.parent_resource
ChildrenResource.parent_resource = ParentsResource


print(ChildrenResource.get_urls())
a = ChildrenResource._get_params()
print(a)


#api.add_resource(root_resource, '/')

#if __name__ == '__main__':
    #app.run(debug=True)
