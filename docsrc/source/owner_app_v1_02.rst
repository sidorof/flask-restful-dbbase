.. code-block:: bash 
    
    # post an order, with the right user
    curl http://localhost:5000/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1" \
        -d '{"ownerId": 1, "description": "to do stuff"}'
    
..

.. code-block:: json 

    {
        "description": "to do stuff",
        "statusId": 0,
        "ownerId": 1,
        "orderedAt": "2020-07-06 10:30:33",
        "id": 1
    }

..
