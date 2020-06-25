.. code-block:: python 

    class OrderCollection(OwnerCollectionResource):
        model_class = Order
    
    
    class OrderResource(OwnerResource):
        model_class = Order
    
    
    class OrderMetaCollection(MetaResource):
        resource_class = OrderCollection
    
    class OrderMeta(MetaResource):
        resource_class = OrderResource
    
    
    # job resources
    class JobCollection(OwnerCollectionResource):
        model_class = Job
    
    
    class JobResource(OwnerResource):
        model_class = Job
    
    
    class JobMetaCollection(MetaResource):
        resource_class = JobCollection
    
    
    class JobMeta(MetaResource):
        resource_class = JobResource
    
    
..