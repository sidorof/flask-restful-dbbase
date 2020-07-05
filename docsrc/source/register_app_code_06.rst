.. code-block:: python 

    SignInResource = create_resource(
        name="SignInResource",
        resource_class=ModelResource,
        model_class=User,
        methods=["post"],
        url_prefix="/",
        url_name="sign-in",
        class_vars={
            "before_commit": {"post": update_last_login}}
    )
    
..