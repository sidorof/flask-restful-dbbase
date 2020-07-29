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
                "finishedAt": null,
                "statusId": 0,
                "startedAt": "2020-07-29 21:41:59",
                "order": {
                    "orderedAt": "2020-07-29 14:41:59",
                    "statusId": 0,
                    "description": "to do different stuff",
                    "ownerId": 1,
                    "id": 1
                },
                "ownerId": 1,
                "id": 1
            },
            {
                "orderId": 1,
                "finishedAt": null,
                "statusId": 0,
                "startedAt": "2020-07-29 21:41:59",
                "order": {
                    "orderedAt": "2020-07-29 14:41:59",
                    "statusId": 0,
                    "description": "to do different stuff",
                    "ownerId": 1,
                    "id": 1
                },
                "ownerId": 1,
                "id": 2
            }
        ]
    }

..
