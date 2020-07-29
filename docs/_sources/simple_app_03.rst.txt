.. code-block:: bash 
    
    # get all books
    curl http://localhost:5000/books \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "Book": [
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
            },
            {
                "title": "The Cell: A Molecular Approach, 4th edition",
                "author": {
                    "firstName": "Geoffrey",
                    "id": 1,
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper"
                },
                "isbn": "978-0878932191",
                "id": 2,
                "authorId": 1,
                "pubYear": 2006
            },
            {
                "title": "The Cell: A Molecular Approach, 7th edition",
                "author": {
                    "firstName": "Geoffrey",
                    "id": 1,
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper"
                },
                "isbn": "978-1605352909",
                "id": 3,
                "authorId": 1,
                "pubYear": 2015
            },
            {
                "title": "The Cell: A Molecular Approach, 9th edition",
                "author": {
                    "firstName": "Geoffrey",
                    "id": 1,
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper"
                },
                "isbn": "978-1605357072",
                "id": 4,
                "authorId": 1,
                "pubYear": 2018
            },
            {
                "title": "Manufacturing Engineering & Technology (7th Edition)",
                "author": {
                    "firstName": "Serope",
                    "id": 2,
                    "lastName": "Kalpakjian",
                    "fullName": "Serope Kalpakjian"
                },
                "isbn": "978-0133128741",
                "id": 5,
                "authorId": 2,
                "pubYear": 2013
            },
            {
                "title": "The Algorithm Design Manual",
                "author": {
                    "firstName": "Steven",
                    "id": 3,
                    "lastName": "Skiena",
                    "fullName": "Steven Skiena"
                },
                "isbn": "0-387-94860-0",
                "id": 6,
                "authorId": 3,
                "pubYear": 1997
            }
        ]
    }

..
