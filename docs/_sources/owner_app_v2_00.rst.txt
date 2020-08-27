.. code-block:: bash 
    
    # post an order, receive a job
    curl http://localhost:5000/api/v2/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1" \
        -d '{"ownerId": 1, "description": "to do stuff"}'
    
..

.. code-block:: JSON 

    {
        "id": 1,
        "startedAt": "2020-08-27 17:38:03",
        "statusId": 0
    }

..
