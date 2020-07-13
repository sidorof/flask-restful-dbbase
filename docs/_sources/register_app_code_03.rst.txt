.. code-block:: python 

    def register_confirm(self, item, status_code):
        """
        This will be used in an after_commit function.
        It always receives an item and the default response status code.
        """
    
        try:
            # use the default status_code for response
            token = encode_token(item.email)
            print(f"the token: {token} would be included in a welcome email")
            return item, status_code
        except:
            # change the status code to something appropriate
            error = {"message": "Problem sending email"}
            return error, 400
    
    def update_last_login(self, item, status_code):
        """
        This function runs in a before commit and updates the user
        record with the current date.
        """
        item.last_login = datetime.now()
        return item, status_code
    
..