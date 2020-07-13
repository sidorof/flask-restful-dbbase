.. code-block:: bash 
    
    # register
    curl http://localhost:5000/register \
        -H "Content-Type: application/json" \
        -d '{
      "username": "iam_user",
      "email": "iam_user@example.com",
      "password": "very_secret"
    }'
    
..

.. code-block:: json 

    {
        "username": "iam_user",
        "email": "iam_user@example.com"
    }

..
