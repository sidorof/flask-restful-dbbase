.. code-block:: python 

    def mock_jwt_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = request.headers.get("Authorization", None)
            if user is not None and user.startswith("User"):
                # we're completely secure, sir
                return fn(*args, **kwargs)
            return {"message": "Unauthorized User"}, 401
    
        return wrapper
    
    
    def get_identity():
        user = request.headers.get("Authorization", None)
        user_id = int(user.split(":")[1])
        return user_id
    
    
..