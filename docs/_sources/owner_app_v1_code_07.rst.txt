.. code-block:: python 

    api.add_resource(OrderCollection, *OrderCollection.get_urls())
    api.add_resource(OrderResource, *OrderResource.get_urls())
    api.add_resource(OrderMetaCollection, *OrderMetaCollection.get_urls())
    api.add_resource(OrderMeta, *OrderMeta.get_urls())
    
    
    if __name__ == "__main__":
        app.run(debug=True)
..