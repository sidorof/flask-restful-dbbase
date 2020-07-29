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
            },
            {
                "title": "The Cell: A Molecular Approach, 4th edition",
                "isbn": "978-0878932191",
                "pubYear": 2006,
                "id": 2,
                "author": {
                    "lastName": "Cooper",
                    "id": 1,
                    "fullName": "Geoffrey Cooper",
                    "firstName": "Geoffrey"
                },
                "authorId": 1
            },
            {
                "title": "The Cell: A Molecular Approach, 7th edition",
                "isbn": "978-1605352909",
                "pubYear": 2015,
                "id": 3,
                "author": {
                    "lastName": "Cooper",
                    "id": 1,
                    "fullName": "Geoffrey Cooper",
                    "firstName": "Geoffrey"
                },
                "authorId": 1
            },
            {
                "title": "The Cell: A Molecular Approach, 9th edition",
                "isbn": "978-1605357072",
                "pubYear": 2018,
                "id": 4,
                "author": {
                    "lastName": "Cooper",
                    "id": 1,
                    "fullName": "Geoffrey Cooper",
                    "firstName": "Geoffrey"
                },
                "authorId": 1
            },
            {
                "title": "Manufacturing Engineering & Technology (7th Edition)",
                "isbn": "978-0133128741",
                "pubYear": 2013,
                "id": 5,
                "author": {
                    "lastName": "Kalpakjian",
                    "id": 2,
                    "fullName": "Serope Kalpakjian",
                    "firstName": "Serope"
                },
                "authorId": 2
            },
            {
                "title": "The Algorithm Design Manual",
                "isbn": "0-387-94860-0",
                "pubYear": 1997,
                "id": 6,
                "author": {
                    "lastName": "Skiena",
                    "id": 3,
                    "fullName": "Steven Skiena",
                    "firstName": "Steven"
                },
                "authorId": 3
            }
        ]
    }

..
