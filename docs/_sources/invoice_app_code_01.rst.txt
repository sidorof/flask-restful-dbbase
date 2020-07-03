.. code-block:: python 

    class InvoiceResource(ModelResource):
        model_class = Invoice
    
        # necessary only if the database does not understand
        #   dates in string form -- such as Sqlite3
        use_date_conversions = True
    
    
..