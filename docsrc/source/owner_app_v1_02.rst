.. code-block:: bash 
    
    # post an order, with the right user
    curl http://localhost:5000/orders \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1" \
        -d '{"ownerId": 1, "description": "to do stuff"}'
    
..

.. code-block:: JSON 

    {
        "statusId": 0,
        "id": 1,
        "ownerId": 1,
        "description": "to do stuff",
        "orderedAt": "2020-07-30 15:30:02"
    }

..
