.. code-block:: bash 
    
    # user receives an email with a URL that
    # contains the token
    curl http://localhost:5000/confirm/ImlhbV91c2VyQGV4YW1wbGUuY29tIg.XwJSEg.SxbKSNHiXhrGaeIBgM8DQdb95fU \
        -H "Content-Type: application/json"
    
..

.. code-block:: json 

    {
        "message": "Welcome to ________!"
    }

..
