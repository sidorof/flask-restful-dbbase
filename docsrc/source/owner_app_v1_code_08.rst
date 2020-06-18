.. code-block:: python 

    api.add_resource(OrderCollection, *OrderCollection.get_urls())
    api.add_resource(OrderResource, *OrderResource.get_urls())
    api.add_resource(OrderMetaCollection, *OrderMetaCollection.get_urls())
    api.add_resource(OrderMeta, *OrderMeta.get_urls())
    
    api.add_resource(JobCollection, *JobCollection.get_urls())
    api.add_resource(JobResource, *JobResource.get_urls())
    api.add_resource(JobMetaCollection, *JobMetaCollection.get_urls())
    api.add_resource(JobMeta, *JobMeta.get_urls())
    
    
    if __name__ == "__main__":
        app.run(debug=True)
..