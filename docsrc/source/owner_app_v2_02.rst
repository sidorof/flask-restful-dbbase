.. code-block:: bash 
    
    # get orders
    curl http://localhost:5000/api/v2/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1"
    
..

.. code-block:: JSON 

    {
        "Order": [
            {
                "orderedAt": "2020-07-29 14:41:59",
                "statusId": 0,
                "description": "to do different stuff",
                "jobs": [
                    {
                        "orderId": 1,
                        "finishedAt": null,
                        "statusId": 0,
                        "startedAt": "2020-07-29 21:41:59",
                        "ownerId": 1,
                        "id": 1
                    },
                    {
                        "orderId": 1,
                        "finishedAt": null,
                        "statusId": 0,
                        "startedAt": "2020-07-29 21:41:59",
                        "ownerId": 1,
                        "id": 2
                    }
                ],
                "ownerId": 1,
                "id": 1
            }
        ]
    }

..
