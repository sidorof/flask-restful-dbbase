.. code-block:: python 

    db.create_all()
    
    # create users
    user = User(
        username="our_main_user",
        password="verysecret",
        email="user_mainexample.com",
    ).save()
    
    user = User(
        username="another_user",
        password="also_quite_secret",
        email="another@example.com",
    ).save()
    
    
..