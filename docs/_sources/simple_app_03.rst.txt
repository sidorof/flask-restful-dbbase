.. code-block:: bash 
    
    # get all books
    curl http://localhost:5000/books \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "Book": [
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
            },
            {
                "author": {
                    "id": 1,
                    "fullName": "Geoffrey Cooper",
                    "firstName": "Geoffrey",
                    "lastName": "Cooper"
                },
                "isbn": "978-0878932191",
                "id": 2,
                "authorId": 1,
                "title": "The Cell: A Molecular Approach, 4th edition",
                "pubYear": 2006
            },
            {
                "author": {
                    "id": 1,
                    "fullName": "Geoffrey Cooper",
                    "firstName": "Geoffrey",
                    "lastName": "Cooper"
                },
                "isbn": "978-1605352909",
                "id": 3,
                "authorId": 1,
                "title": "The Cell: A Molecular Approach, 7th edition",
                "pubYear": 2015
            },
            {
                "author": {
                    "id": 1,
                    "fullName": "Geoffrey Cooper",
                    "firstName": "Geoffrey",
                    "lastName": "Cooper"
                },
                "isbn": "978-1605357072",
                "id": 4,
                "authorId": 1,
                "title": "The Cell: A Molecular Approach, 9th edition",
                "pubYear": 2018
            },
            {
                "author": {
                    "id": 2,
                    "fullName": "Serope Kalpakjian",
                    "firstName": "Serope",
                    "lastName": "Kalpakjian"
                },
                "isbn": "978-0133128741",
                "id": 5,
                "authorId": 2,
                "title": "Manufacturing Engineering & Technology (7th Edition)",
                "pubYear": 2013
            },
            {
                "author": {
                    "id": 3,
                    "fullName": "Steven Skiena",
                    "firstName": "Steven",
                    "lastName": "Skiena"
                },
                "isbn": "0-387-94860-0",
                "id": 6,
                "authorId": 3,
                "title": "The Algorithm Design Manual",
                "pubYear": 1997
            }
        ]
    }

..
