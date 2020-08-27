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
                "description": "to do different stuff",
                "orderedAt": "2020-08-27 10:38:03",
                "statusId": 0,
                "ownerId": 1,
                "id": 1,
                "jobs": [
                    {
                        "startedAt": "2020-08-27 17:38:03",
                        "finishedAt": null,
                        "statusId": 0,
                        "ownerId": 1,
                        "orderId": 1,
                        "id": 1
                    },
                    {
                        "startedAt": "2020-08-27 17:38:03",
                        "finishedAt": null,
                        "statusId": 0,
                        "ownerId": 1,
                        "orderId": 1,
                        "id": 2
                    }
                ]
            }
        ]
    }

..
