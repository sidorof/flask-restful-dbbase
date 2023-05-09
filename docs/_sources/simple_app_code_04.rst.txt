.. code-block:: python 

    api.add_resource(AuthorCollection, *AuthorCollection.get_urls())
    api.add_resource(AuthorResource, *AuthorResource.get_urls())
    api.add_resource(AuthorMetaCollection, *AuthorMetaCollection.get_urls())
    api.add_resource(AuthorMeta, *AuthorMeta.get_urls())
    
    api.add_resource(BookCollection, *BookCollection.get_urls())
    api.add_resource(BookResource, *BookResource.get_urls())
    api.add_resource(BookMetaCollection, *BookMetaCollection.get_urls())
    api.add_resource(BookMeta, *BookMeta.get_urls())
    
    
    if __name__ == "__main__":
        app.run(debug=True, port=5000)
..