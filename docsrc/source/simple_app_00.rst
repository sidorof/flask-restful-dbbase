.. code-block:: bash 
    
    # get a book
    curl http://localhost:5000/books/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "title": "The Cell: A Molecular Approach, 3rd edition",
        "author": {
            "firstName": "Geoffrey",
            "id": 1,
            "lastName": "Cooper",
            "fullName": "Geoffrey Cooper"
        },
        "isbn": "0-87893-214-3",
        "id": 1,
        "authorId": 1,
        "pubYear": 2004
    }

..
