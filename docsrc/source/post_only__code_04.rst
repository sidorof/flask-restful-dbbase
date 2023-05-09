.. code-block:: python 

    # response associated with a POST.
    meta_doc = MetaDoc(
        resource_class=PostOnlyResource,
        methods=[
            MethodDoc(
                method="post",
                after_commit="Here we can say a few words about the process",
                use_default_response=False,
                responses=[{"messsage": "Here we can describe the response"}],
            )
        ],
    )
    PostOnlyResource.meta_doc = meta_doc
    
    
    class PostOnlyMetaResource(MetaResource):
        resource_class = PostOnlyResource
    
    
..