.. code-block:: python 

    PostOnlyResource = create_resource(
        name="PostOnlyResource",
        resource_class=ModelResource,
        model_class=AModel,
        methods=["post"],
        url_prefix="/",
        url_name="a-model-command",
        class_vars={
            "after_commit": {"post": after_commit},
        },
    )
    
..