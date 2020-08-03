.. code-block:: python 

    # response associated with a POST.
    meta_doc = MetaDoc(
        after_commit={
            "post": "This now returns a custom message"
        },
        excludes=["post"]
    )
    PostOnlyResource.meta_doc = meta_doc
    
    class PostOnlyMetaResource(MetaResource):
        resource_class = PostOnlyResource
    
..