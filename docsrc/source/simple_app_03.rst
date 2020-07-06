.. code-block:: bash 
    
    # get all books
    curl http://localhost:5000/books \
        -H "Content-Type: application/json"
    
..

.. code-block:: json 

    {
        "Book": [
            {
                "isbn": "0-87893-214-3",
                "id": 1,
                "title": "The Cell: A Molecular Approach, 3rd edition",
                "author": {
                    "firstName": "Geoffrey",
                    "id": 1,
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper"
                },
                "authorId": 1,
                "pubYear": 2004
            },
            {
                "isbn": "978-0878932191",
                "id": 2,
                "title": "The Cell: A Molecular Approach, 4th edition",
                "author": {
                    "firstName": "Geoffrey",
                    "id": 1,
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper"
                },
                "authorId": 1,
                "pubYear": 2006
            },
            {
                "isbn": "978-1605352909",
                "id": 3,
                "title": "The Cell: A Molecular Approach, 7th edition",
                "author": {
                    "firstName": "Geoffrey",
                    "id": 1,
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper"
                },
                "authorId": 1,
                "pubYear": 2015
            },
            {
                "isbn": "978-1605357072",
                "id": 4,
                "title": "The Cell: A Molecular Approach, 9th edition",
                "author": {
                    "firstName": "Geoffrey",
                    "id": 1,
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper"
                },
                "authorId": 1,
                "pubYear": 2018
            },
            {
                "isbn": "978-0133128741",
                "id": 5,
                "title": "Manufacturing Engineering & Technology (7th Edition)",
                "author": {
                    "firstName": "Serope",
                    "id": 2,
                    "lastName": "Kalpakjian",
                    "fullName": "Serope Kalpakjian"
                },
                "authorId": 2,
                "pubYear": 2013
            },
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
        ]
    }

..
