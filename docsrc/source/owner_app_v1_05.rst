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
                "statusId": 0,
                "id": 1,
                "ownerId": 1,
                "description": "to do stuff",
                "orderedAt": "2020-07-30 15:30:02"
            }
        ]
    }

..
