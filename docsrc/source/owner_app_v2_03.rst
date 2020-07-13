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
                "orderId": 1,
                "id": 1,
                "statusId": 0,
                "finishedAt": null,
                "startedAt": "2020-07-13 21:20:37",
                "order": {
                    "orderedAt": "2020-07-13 14:20:37",
                    "ownerId": 1,
                    "id": 1,
                    "statusId": 0,
                    "description": "to do different stuff"
                }
            },
            {
                "ownerId": 1,
                "orderId": 1,
                "id": 2,
                "statusId": 0,
                "finishedAt": null,
                "startedAt": "2020-07-13 21:20:37",
                "order": {
                    "orderedAt": "2020-07-13 14:20:37",
                    "ownerId": 1,
                    "id": 1,
                    "statusId": 0,
                    "description": "to do different stuff"
                }
            }
        ]
    }

..
