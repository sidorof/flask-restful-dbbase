.. code-block:: bash 
    
    # put an order, receive a job
    curl --request PUT http://localhost:5000/api/v2/orders/1 \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1" \
        -d '{"ownerId": 1, "description": "to do different stuff"}'
    
..

.. code-block:: JSON 

    {
        "id": 2,
        "startedAt": "2020-08-27 17:38:03",
        "statusId": 0
    }

..
