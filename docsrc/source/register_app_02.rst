.. code-block:: bash 
    
    # Sign-in
    curl http:/localhost:5000/sign-in \
        -H "Content-Type: application/json" \
        -d '{"username": "iam_user", "password": "very_secret"}'
    
    
..

.. code-block:: json 

    {
        "message": [
            {
                "missing_columns": [
                    "email"
                ]
            }
        ]
    }

..
