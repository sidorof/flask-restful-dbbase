.. code-block:: bash 
    
    # get orders, with authorization, right user
    curl http://localhost:5000/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1"
    
..

.. code-block:: JSON 

    {
        "Order": [
            {
                "description": "to do stuff",
                "id": 1,
                "ownerId": 1,
                "statusId": 0,
                "orderedAt": "2020-08-27 10:37:47"
            }
        ]
    }

..
