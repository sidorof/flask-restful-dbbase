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
            },
            {
                "author": {
                    "firstName": "Geoffrey",
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper",
                    "id": 1
                },
                "title": "The Cell: A Molecular Approach, 4th edition",
                "authorId": 1,
                "id": 2,
                "isbn": "978-0878932191",
                "pubYear": 2006
            },
            {
                "author": {
                    "firstName": "Geoffrey",
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper",
                    "id": 1
                },
                "title": "The Cell: A Molecular Approach, 7th edition",
                "authorId": 1,
                "id": 3,
                "isbn": "978-1605352909",
                "pubYear": 2015
            },
            {
                "author": {
                    "firstName": "Geoffrey",
                    "lastName": "Cooper",
                    "fullName": "Geoffrey Cooper",
                    "id": 1
                },
                "title": "The Cell: A Molecular Approach, 9th edition",
                "authorId": 1,
                "id": 4,
                "isbn": "978-1605357072",
                "pubYear": 2018
            },
            {
                "author": {
                    "firstName": "Serope",
                    "lastName": "Kalpakjian",
                    "fullName": "Serope Kalpakjian",
                    "id": 2
                },
                "title": "Manufacturing Engineering & Technology (7th Edition)",
                "authorId": 2,
                "id": 5,
                "isbn": "978-0133128741",
                "pubYear": 2013
            },
            {
                "author": {
                    "firstName": "Steven",
                    "lastName": "Skiena",
                    "fullName": "Steven Skiena",
                    "id": 3
                },
                "title": "The Algorithm Design Manual",
                "authorId": 3,
                "id": 6,
                "isbn": "0-387-94860-0",
                "pubYear": 1997
            }
        ]
    }

..
