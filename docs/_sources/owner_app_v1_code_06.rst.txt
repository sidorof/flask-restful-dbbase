.. code-block:: python 

    class OrderCollection(OwnerCollectionResource):
        model_class = Order
    
    
    class OrderResource(OwnerResource):
        model_class = Order
    
    
    class OrderMetaCollection(MetaResource):
        resource_class = OrderCollection
    
    
    class OrderMeta(MetaResource):
        resource_class = OrderResource
    
    
    
..