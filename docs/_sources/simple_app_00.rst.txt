.. code-block:: bash 
    
    # get a book
    curl http://localhost:5000/books/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "author": {
            "id": 1,
            "fullName": "Geoffrey Cooper",
            "firstName": "Geoffrey",
            "lastName": "Cooper"
        },
        "isbn": "0-87893-214-3",
        "id": 1,
        "authorId": 1,
        "title": "The Cell: A Molecular Approach, 3rd edition",
        "pubYear": 2004
    }

..
