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
                "orderedAt": "2020-06-24 16:15:30",
                "description": "to do stuff",
                "id": 1,
                "statusId": 0,
                "ownerId": 1
            }
        ]
    }

..
