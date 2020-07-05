.. code-block:: python 

    RegisterResource = create_resource(
        name="RegisterResource",
        resource_class=ModelResource,
        model_class=User,
        methods=["post"],
        url_prefix="/",
        url_name="register",
        class_vars = {
            "after_commit": {
                "post": register_confirm
            }
        }
    )
    
..