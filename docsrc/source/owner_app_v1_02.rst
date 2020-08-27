.. code-block:: bash 
    
    # post an order, with the right user
    curl http://localhost:5000/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1" \
        -d '{"ownerId": 1, "description": "to do stuff"}'
    
..

.. code-block:: JSON 

    {
        "description": "to do stuff",
        "id": 1,
        "ownerId": 1,
        "statusId": 0,
        "orderedAt": "2020-08-27 10:37:47"
    }

..
