.. code-block:: python 

    def after_commit(self, item, status_code):
        """
        This will be used in an after_commit function.
    
        In this case, the process is diverted to a
        message, new status code and the method exits with
        this message.
        """
        # processing takes place here
        payload = {
            "message": "This is no longer a REST resource. We can do anything.",
            "data": item.to_dict(),
        }
    
        return False, payload, 419
    
    
..