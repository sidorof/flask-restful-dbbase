.. code-block:: python 

    class OrderResource(OwnerResource):
        model_class = Order
        url_prefix = "/api/v2"
    
        serial_fields = {
            "post": {Job: ['id', "started_at", "status_id"]},
            "put": {Job: ['id', "started_at", "status_id"]},
        }
    
        after_commit = {
            "post": create_job,
            "put": create_job
        }
    
..