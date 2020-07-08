.. code-block:: bash 
    
    # post a book with valid data
    curl http://localhost:5000/books \
        -H "Content-Type: application/json" \
        -d '{"authorId": 3,
             "title": "The Algorithm Design Manual",
             "pubYear": 1997,
             "isbn": "0-387-94860-0"}'
    
..

.. code-block:: json 

    {
        "isbn": "0-387-94860-0",
        "id": 6,
        "title": "The Algorithm Design Manual",
        "author": {
            "firstName": "Steven",
            "id": 3,
            "lastName": "Skiena",
            "fullName": "Steven Skiena"
        },
        "authorId": 3,
        "pubYear": 1997
    }

..
