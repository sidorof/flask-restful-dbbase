.. code-block:: bash 
    
    # get orders, with authorization, right user
    curl http://localhost:5000/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1"
    
..

.. code-block:: json 

    {
        "Order": [
            {
                "description": "to do stuff",
                "statusId": 0,
                "ownerId": 1,
                "orderedAt": "2020-07-06 10:30:33",
                "id": 1
            }
        ]
    }

..
