.. code-block:: python 

    api.add_resource(
        InvoiceCollectionResource, *InvoiceCollectionResource.get_urls()
    )
    api.add_resource(InvoiceResource, *InvoiceResource.get_urls())
    api.add_resource(
        InvoiceItemCollectionResource, *InvoiceItemCollectionResource.get_urls()
    )
    api.add_resource(InvoiceItemResource, *InvoiceResource.get_urls())
    
    api.add_resource(InvoiceMeta, *InvoiceMeta.get_urls())
    api.add_resource(InvoiceMetaCollection, *InvoiceMetaCollection.get_urls())
    api.add_resource(InvoiceItemMeta, *InvoiceItemMeta.get_urls())
    api.add_resource(
        InvoiceItemMetaCollection, *InvoiceItemMetaCollection.get_urls()
    )
    
    
    if __name__ == "__main__":
        app.run(debug=True)
..