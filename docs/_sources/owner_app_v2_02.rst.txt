.. code-block:: bash 
    
    # get orders
    curl http://localhost:5000/api/v2/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1"
    
..

.. code-block:: json 

    {
        "Order": [
            {
                "jobs": [
                    {
                        "startedAt": "2020-06-27 00:40:46",
                        "orderId": 1,
                        "finishedAt": null,
                        "ownerId": 1,
                        "statusId": 0,
                        "id": 1
                    },
                    {
                        "startedAt": "2020-06-27 00:40:46",
                        "orderId": 1,
                        "finishedAt": null,
                        "ownerId": 1,
                        "statusId": 0,
                        "id": 2
                    }
                ],
                "description": "to do different stuff",
                "orderedAt": "2020-06-26 17:40:46",
                "ownerId": 1,
                "statusId": 0,
                "id": 1
            }
        ]
    }

..
