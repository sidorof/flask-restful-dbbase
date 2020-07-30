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
                "ownerId": 1,
                "order": {
                    "orderedAt": "2020-07-30 15:30:35",
                    "description": "to do different stuff",
                    "statusId": 0,
                    "id": 1,
                    "ownerId": 1
                },
                "statusId": 0,
                "id": 1,
                "orderId": 1,
                "finishedAt": null,
                "startedAt": "2020-07-30 22:30:35"
            },
            {
                "ownerId": 1,
                "order": {
                    "orderedAt": "2020-07-30 15:30:35",
                    "description": "to do different stuff",
                    "statusId": 0,
                    "id": 1,
                    "ownerId": 1
                },
                "statusId": 0,
                "id": 2,
                "orderId": 1,
                "finishedAt": null,
                "startedAt": "2020-07-30 22:30:35"
            }
        ]
    }

..
