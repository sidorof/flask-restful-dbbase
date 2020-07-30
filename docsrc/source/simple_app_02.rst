.. code-block:: bash 
    
    # post a book with valid data
    curl http://localhost:5000/books \
        -H "Content-Type: application/json" \
        -d '{"authorId": 3,
             "title": "The Algorithm Design Manual",
             "pubYear": 1997,
             "isbn": "0-387-94860-0"}'
    
..

.. code-block:: JSON 

    {
        "pubYear": 1997,
        "authorId": 3,
        "id": 6,
        "author": {
            "lastName": "Skiena",
            "id": 3,
            "firstName": "Steven",
            "fullName": "Steven Skiena"
        },
        "title": "The Algorithm Design Manual",
        "isbn": "0-387-94860-0"
    }

..
