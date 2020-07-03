.. code-block:: python 

    class InvoiceCollectionResource(CollectionModelResource):
        model_class = Invoice
    
    
    class InvoiceItemResource(ModelResource):
        model_class = InvoiceItem
    
    
    class InvoiceItemCollectionResource(ModelResource):
        model_class = InvoiceItem
    
    
    # create meta resources
    class InvoiceMeta(MetaResource):
        resource_class = InvoiceResource
    
    
    class InvoiceMetaCollection(MetaResource):
        resource_class = InvoiceResource
    
    
    class InvoiceItemMeta(MetaResource):
        resource_class = InvoiceItemResource
    
    
    class InvoiceItemMetaCollection(MetaResource):
        resource_class = InvoiceItemResource
    
    
..