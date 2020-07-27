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
                "orderedAt": "2020-07-26 17:30:09",
                "ownerId": 1,
                "id": 1,
                "jobs": [
                    {
                        "ownerId": 1,
                        "id": 1,
                        "startedAt": "2020-07-27 00:30:09",
                        "statusId": 0,
                        "finishedAt": null,
                        "orderId": 1
                    },
                    {
                        "ownerId": 1,
                        "id": 2,
                        "startedAt": "2020-07-27 00:30:09",
                        "statusId": 0,
                        "finishedAt": null,
                        "orderId": 1
                    }
                ],
                "statusId": 0,
                "description": "to do different stuff"
            }
        ]
    }

..
