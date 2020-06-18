.. code-block:: bash 
    
    # get orders, with authorization, right user
    curl -H "Content-Type: application/json" \
         -H "Authorization: User:1" \
         http://localhost:5000/orders
    
..

.. code-block:: json 

    {
        "Order": [
            {
                "ownerId": 1,
                "id": 1,
                "orderedAt": "2020-06-16 07:35:41",
                "description": "to do stuff",
                "statusId": 0
            }
        ]
    }

..
