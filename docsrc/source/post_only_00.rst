.. code-block:: bash 
    
    # create an entry
    curl http://localhost:5000/a-model-command \
        -H "Content-Type: application/json" \
        -d '{"description": "A test", "num_variable": 42}'
    
..

.. code-block:: JSON 

    {
        "message": "This is no longer a REST resource. We can do anything.",
        "data": {
            "description": "A test",
            "id": 1,
            "numVariable": 42
        }
    }

..
