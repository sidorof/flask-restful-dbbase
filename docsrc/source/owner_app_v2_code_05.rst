.. code-block:: python 

    class JobCollection(OwnerCollectionResource):
        model_class = Job
        url_prefix = "/api/v2"
    
    
    class JobResource(OwnerResource):
        model_class = Job
        url_prefix = "/api/v2"
    
    
    class JobMetaCollection(MetaResource):
        resource_class = JobCollection
    
    class JobMeta(MetaResource):
        resource_class = JobResource
    
    
..