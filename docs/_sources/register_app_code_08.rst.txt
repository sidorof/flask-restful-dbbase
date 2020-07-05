.. code-block:: python 

    api.add_resource(RegisterResource, *RegisterResource.get_urls())
    api.add_resource(SignInResource, *SignInResource.get_urls())
    api.add_resource(ConfirmResource, '/confirm/<token>')
    
    api.add_resource(RegisterMetaResource, *RegisterMetaResource.get_urls())
    api.add_resource(SignInMetaResource, *SignInMetaResource.get_urls())
    
    
    if __name__ == "__main__":
        app.run(debug=True)
..