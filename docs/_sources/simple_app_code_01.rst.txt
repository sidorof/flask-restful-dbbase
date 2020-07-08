.. code-block:: python 

    author = Author(first_name="Geoffrey", last_name="Cooper").save()
    
    book = Book(
        isbn="0-87893-214-3",
        title="The Cell: A Molecular Approach, 3rd edition",
        pub_year=2004,
        author_id=author.id,
    ).save()
    book = Book(
        isbn="978-0878932191",
        title="The Cell: A Molecular Approach, 4th edition",
        pub_year=2006,
        author_id=author.id,
    ).save()
    
    book = Book(
        isbn="978-1605352909",
        title="The Cell: A Molecular Approach, 7th edition",
        pub_year=2015,
        author_id=author.id,
    ).save()
    
    book = Book(
        isbn="978-1605357072",
        title="The Cell: A Molecular Approach, 9th edition",
        pub_year=2018,
        author_id=author.id,
    ).save()
    
    author = Author(first_name="Serope", last_name="Kalpakjian").save()
    
    book = Book(
        isbn="978-0133128741",
        title="Manufacturing Engineering & Technology (7th Edition)",
        pub_year=2013,
        author_id=author.id,
    ).save()
    
    author = Author(first_name="Steven", last_name="Skiena").save()
    
    
..