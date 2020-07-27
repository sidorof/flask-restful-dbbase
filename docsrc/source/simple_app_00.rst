.. code-block:: bash 
    
    # get a book
    curl http://localhost:5000/books/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "pubYear": 2004,
        "authorId": 1,
        "title": "The Cell: A Molecular Approach, 3rd edition",
        "id": 1,
        "isbn": "0-87893-214-3",
        "author": {
            "firstName": "Geoffrey",
            "fullName": "Geoffrey Cooper",
            "id": 1,
            "lastName": "Cooper"
        }
    }

..
