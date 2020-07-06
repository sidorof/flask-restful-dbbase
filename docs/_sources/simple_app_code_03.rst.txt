.. code-block:: python 

    class BookMetaCollection(MetaResource):
        resource_class = BookCollection
    
    class BookMeta(MetaResource):
        resource_class = BookResource
    
    class AuthorMetaCollection(MetaResource):
        resource_class = AuthorCollection
    
    class AuthorMeta(MetaResource):
        resource_class = AuthorResource
    
..