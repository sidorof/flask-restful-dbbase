.. code-block:: bash 
    
    # get a book
    curl http://localhost:5000/books/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "title": "The Cell: A Molecular Approach, 3rd edition",
        "isbn": "0-87893-214-3",
        "pubYear": 2004,
        "id": 1,
        "author": {
            "lastName": "Cooper",
            "id": 1,
            "fullName": "Geoffrey Cooper",
            "firstName": "Geoffrey"
        },
        "authorId": 1
    }

..
