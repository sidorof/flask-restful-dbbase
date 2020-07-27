.. code-block:: bash 
    
    # post a book, but with invalid data
    curl http://localhost:5000/books \
        -H "Content-Type: application/json" \
        -d '{"authorId": 1,
             "title": "this is a test woah, this is really a long title, woah, this is really a long title, woah, this is really a long title, woah, this is really a long title, woah, this is really a long title "}'
    
..

.. code-block:: JSON 

    {
        "message": [
            {
                "title": "The data exceeds the maximum length 100"
            },
            {
                "missing_columns": [
                    "pub_year"
                ]
            }
        ]
    }

..
