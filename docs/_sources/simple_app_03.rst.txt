.. code-block:: bash 
    
    # get all books
    curl http://localhost:5000/books \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "Book": [
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
            },
            {
                "pubYear": 2006,
                "authorId": 1,
                "id": 2,
                "author": {
                    "lastName": "Cooper",
                    "id": 1,
                    "firstName": "Geoffrey",
                    "fullName": "Geoffrey Cooper"
                },
                "title": "The Cell: A Molecular Approach, 4th edition",
                "isbn": "978-0878932191"
            },
            {
                "pubYear": 2015,
                "authorId": 1,
                "id": 3,
                "author": {
                    "lastName": "Cooper",
                    "id": 1,
                    "firstName": "Geoffrey",
                    "fullName": "Geoffrey Cooper"
                },
                "title": "The Cell: A Molecular Approach, 7th edition",
                "isbn": "978-1605352909"
            },
            {
                "pubYear": 2018,
                "authorId": 1,
                "id": 4,
                "author": {
                    "lastName": "Cooper",
                    "id": 1,
                    "firstName": "Geoffrey",
                    "fullName": "Geoffrey Cooper"
                },
                "title": "The Cell: A Molecular Approach, 9th edition",
                "isbn": "978-1605357072"
            },
            {
                "pubYear": 2013,
                "authorId": 2,
                "id": 5,
                "author": {
                    "lastName": "Kalpakjian",
                    "id": 2,
                    "firstName": "Serope",
                    "fullName": "Serope Kalpakjian"
                },
                "title": "Manufacturing Engineering & Technology (7th Edition)",
                "isbn": "978-0133128741"
            },
            {
                "pubYear": 1997,
                "authorId": 3,
                "id": 6,
                "author": {
                    "lastName": "Skiena",
                    "id": 3,
                    "firstName": "Steven",
                    "fullName": "Steven Skiena"
                },
                "title": "The Algorithm Design Manual",
                "isbn": "0-387-94860-0"
            }
        ]
    }

..
