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
                "title": "The Cell: A Molecular Approach, 3rd edition",
                "id": 1,
                "isbn": "0-87893-214-3",
                "author": {
                    "firstName": "Geoffrey",
                    "fullName": "Geoffrey Cooper",
                    "id": 1,
                    "lastName": "Cooper"
                }
            },
            {
                "pubYear": 2006,
                "authorId": 1,
                "title": "The Cell: A Molecular Approach, 4th edition",
                "id": 2,
                "isbn": "978-0878932191",
                "author": {
                    "firstName": "Geoffrey",
                    "fullName": "Geoffrey Cooper",
                    "id": 1,
                    "lastName": "Cooper"
                }
            },
            {
                "pubYear": 2015,
                "authorId": 1,
                "title": "The Cell: A Molecular Approach, 7th edition",
                "id": 3,
                "isbn": "978-1605352909",
                "author": {
                    "firstName": "Geoffrey",
                    "fullName": "Geoffrey Cooper",
                    "id": 1,
                    "lastName": "Cooper"
                }
            },
            {
                "pubYear": 2018,
                "authorId": 1,
                "title": "The Cell: A Molecular Approach, 9th edition",
                "id": 4,
                "isbn": "978-1605357072",
                "author": {
                    "firstName": "Geoffrey",
                    "fullName": "Geoffrey Cooper",
                    "id": 1,
                    "lastName": "Cooper"
                }
            },
            {
                "pubYear": 2013,
                "authorId": 2,
                "title": "Manufacturing Engineering & Technology (7th Edition)",
                "id": 5,
                "isbn": "978-0133128741",
                "author": {
                    "firstName": "Serope",
                    "fullName": "Serope Kalpakjian",
                    "id": 2,
                    "lastName": "Kalpakjian"
                }
            },
            {
                "pubYear": 1997,
                "authorId": 3,
                "title": "The Algorithm Design Manual",
                "id": 6,
                "isbn": "0-387-94860-0",
                "author": {
                    "firstName": "Steven",
                    "fullName": "Steven Skiena",
                    "id": 3,
                    "lastName": "Skiena"
                }
            }
        ]
    }

..
