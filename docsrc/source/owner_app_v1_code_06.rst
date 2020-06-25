.. code-block:: python 

    class OwnerResource(ModelResource):
        """
        Pretend that jwt is being used for determining
        authenticated users.
    
        The basic strategy for process_{method}_input functions:
    
        Returns:
            status: (bool) : Success or failure
            data: (obj) :  if success, the data
                           if failure (explanation, status_code)
    
        That means the response.status_code can be tailored to fit your
        scenario.
    
        """
    
        method_decorators = [mock_jwt_required]
    
        def process_get_input(self, query, data, kwargs):
            """
            This function runs in the GET method with access to
            the Model.query object.
            """
            user_id = get_identity()
            if user_id:
                query = query.filter_by(owner_id=user_id)
                return True, (query, data)
    
            return False, ({"message": "Not found"}, 404)
    
        def process_post_input(self, data):
            """
            This function runs in the POST method with access to
            the data included with the request.
            """
            user_id = get_identity()
            owner_id = data.get("ownerId", None)
            if owner_id:
                if int(owner_id) == user_id:
                    return True, data
    
            return False, ({"message": "The user id does not match the owner id"}, 400)
    
    
        def process_put_input(self, query, data, kwargs):
            """
            This function runs in the PUT method with access to
            the data included with the request.
            """
            user_id = get_identity()
            owner_id = data.get("ownerId", None)
            if owner_id:
                if int(owner_id) == user_id:
                    return True, data
    
            return False, ({"message": "The user id does not match the owner id"}, 400)
    
        def process_patch_input(self, query, data, kwargs):
            """
            This function runs in the PATCH method with access to
            the data included with the request.
            """
            user_id = get_identity()
            owner_id = data.get("ownerId", None)
            if owner_id:
                if int(owner_id) == user_id:
                    return True, data
    
            return False, ({"message": "The user id does not match the owner id"}, 400)
    
        def process_delete_input(self, query, kwargs):
            """
            This function runs in the DELETE method.
            """
            user_id = get_identity()
            if user_id:
                query = query.filter_by(owner_id=user_id)
                return True, query
    
            return False, ("Not found", 404)
    
    class OwnerCollectionResource(CollectionModelResource):
        """
        Pretend that jwt is being used for determine authenticated users.
        """
    
        method_decorators = [mock_jwt_required]
    
        def process_get_input(self, query, data):
            user_id = get_identity()
            if user_id:
                query = query.filter_by(owner_id=user_id)
                return True, (query, data)
    
            return False, ("The user id is not authorized", 400)
    
    
..