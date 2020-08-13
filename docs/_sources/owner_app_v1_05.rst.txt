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
                "id": 1,
                "ownerId": 1,
                "statusId": 0,
                "orderedAt": "2020-08-13 15:04:06",
                "description": "to do stuff"
            }
        ]
    }

..
