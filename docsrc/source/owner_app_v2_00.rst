.. code-block:: bash 
    
    # post an order, receive a job
    curl http://localhost:5000/api/v2/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1" \
        -d '{"ownerId": 1, "description": "to do stuff"}'
    
..

.. code-block:: json 

    {
        "id": 1,
        "startedAt": "2020-06-27 00:40:46",
        "statusId": 0
    }

..
