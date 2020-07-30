.. code-block:: bash 
    
    # get a book
    curl http://localhost:5000/books/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "pubYear": 2004,
        "authorId": 1,
        "id": 1,
        "author": {
            "lastName": "Cooper",
            "id": 1,
            "firstName": "Geoffrey",
            "fullName": "Geoffrey Cooper"
        },
        "title": "The Cell: A Molecular Approach, 3rd edition",
        "isbn": "0-87893-214-3"
    }

..
