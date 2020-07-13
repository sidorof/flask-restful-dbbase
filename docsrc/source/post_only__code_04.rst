.. code-block:: python 

    api.add_resource(PostOnlyResource, *PostOnlyResource.get_urls())
    
    
    if __name__ == "__main__":
        app.run(debug=True)
..