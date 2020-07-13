.. code-block:: python 

    class BookCollection(CollectionModelResource):
        model_class = Book
    
    
    class BookResource(ModelResource):
        model_class = Book
    
    
    class AuthorCollection(CollectionModelResource):
        model_class = Author
    
    
    class AuthorResource(ModelResource):
        model_class = Author
    
    
..