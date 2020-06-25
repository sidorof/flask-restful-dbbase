.. code-block:: bash 
    
    # post an order, with the right user
    curl http://localhost:5000/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1" \
        -d '{"ownerId": 1, "description": "to do stuff"}'
    
..

.. code-block:: json 

    {
        "orderedAt": "2020-06-24 16:15:30",
        "description": "to do stuff",
        "id": 1,
        "statusId": 0,
        "ownerId": 1
    }

..
