.. code-block:: python 

    class ConfirmResource(Resource):
        """
        This resource is best without ModelResource.
    
        * It uses the User model, but does not enforce the User.id
        to be part of the URL.
        * The confirm token is ephemeral, no need to save it.
        * It is easier to simply do the user query directly.
        * It does not need to return user information.
        """
        def get(self, token):
    
            try:
                email = confirm_token(token)
            except:
                msg = "Confirmation token has either expired or is invalid"
                return {"message": msg}, 401
    
            user = User.query.filter(User.email == email).first()
    
            if user is not None:
    
                user.is_active = True
                user.save()
                # front end would then redirect to sign-in
                return {"message": "Welcome to ________!"}, 200
    
            return {"message": "This email is not valid"}, 401
    
    
..