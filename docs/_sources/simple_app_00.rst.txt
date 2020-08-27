.. code-block:: bash 
    
    # get a book
    curl http://localhost:5000/books/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "author": {
            "firstName": "Geoffrey",
            "lastName": "Cooper",
            "fullName": "Geoffrey Cooper",
            "id": 1
        },
        "title": "The Cell: A Molecular Approach, 3rd edition",
        "authorId": 1,
        "id": 1,
        "isbn": "0-87893-214-3",
        "pubYear": 2004
    }

..
