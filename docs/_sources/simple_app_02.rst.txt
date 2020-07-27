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
        "title": "The Algorithm Design Manual",
        "id": 6,
        "isbn": "0-387-94860-0",
        "author": {
            "firstName": "Steven",
            "fullName": "Steven Skiena",
            "id": 3,
            "lastName": "Skiena"
        }
    }

..
