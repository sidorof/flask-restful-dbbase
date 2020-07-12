.. code-block:: python 

    def create_job(self, order, status_code):
        """
        This function creates a processing job from an order.
    
        It runs after the order is saved to the database, then
        creates a job and submits it to processing.
    
        Args:
            order: (obj) : The order that is to be processed.
            status_code: (int) :
        Returns:
            return_status: (bool) : True to coninue,
                False  to return just a message
            job: (obj) : The job that is created.
            status_code: (int) : The new response status
            code.
        """
    
        job = Job(owner_id=order.owner_id, order_id=order.id).save()
        status_code = 202
        # this is where you send the job to queue
    
        return True, job, status_code
    
    
..