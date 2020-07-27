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
                "id": 1,
                "order": {
                    "orderedAt": "2020-07-26 17:30:09",
                    "ownerId": 1,
                    "id": 1,
                    "statusId": 0,
                    "description": "to do different stuff"
                },
                "startedAt": "2020-07-27 00:30:09",
                "statusId": 0,
                "finishedAt": null,
                "orderId": 1
            },
            {
                "ownerId": 1,
                "id": 2,
                "order": {
                    "orderedAt": "2020-07-26 17:30:09",
                    "ownerId": 1,
                    "id": 1,
                    "statusId": 0,
                    "description": "to do different stuff"
                },
                "startedAt": "2020-07-27 00:30:09",
                "statusId": 0,
                "finishedAt": null,
                "orderId": 1
            }
        ]
    }

..
