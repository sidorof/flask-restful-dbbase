.. code-block:: python 

    class OrderCollection(OwnerCollectionResource):
        model_class = Order
        url_prefix = "/api/v2"
    
..