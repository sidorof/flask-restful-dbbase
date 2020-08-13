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
                "statusId": 0,
                "id": 1,
                "jobs": [
                    {
                        "orderId": 1,
                        "statusId": 0,
                        "id": 1,
                        "finishedAt": null,
                        "startedAt": "2020-08-13 22:04:19",
                        "ownerId": 1
                    },
                    {
                        "orderId": 1,
                        "statusId": 0,
                        "id": 2,
                        "finishedAt": null,
                        "startedAt": "2020-08-13 22:04:19",
                        "ownerId": 1
                    }
                ],
                "ownerId": 1,
                "orderedAt": "2020-08-13 15:04:19",
                "description": "to do different stuff"
            }
        ]
    }

..
