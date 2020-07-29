.. code-block:: bash 
    
    # get jobs
    curl http://localhost:5000/api/v2/jobs \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1"
    
..

.. code-block:: JSON 

    {
        "Job": [
            {
                "orderId": 1,
                "order": {
                    "description": "to do different stuff",
                    "ownerId": 1,
                    "statusId": 0,
                    "orderedAt": "2020-07-29 14:31:07",
                    "id": 1
                },
                "ownerId": 1,
                "statusId": 0,
                "id": 1,
                "startedAt": "2020-07-29 21:31:07",
                "finishedAt": null
            },
            {
                "orderId": 1,
                "order": {
                    "description": "to do different stuff",
                    "ownerId": 1,
                    "statusId": 0,
                    "orderedAt": "2020-07-29 14:31:07",
                    "id": 1
                },
                "ownerId": 1,
                "statusId": 0,
                "id": 2,
                "startedAt": "2020-07-29 21:31:08",
                "finishedAt": null
            }
        ]
    }

..
