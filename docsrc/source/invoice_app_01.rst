.. code-block:: bash 
    
    # get an invoice
    curl http://localhost:5000/invoices/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "invoiceItems": [
            {
                "units": 1,
                "unitPrice": 20.0,
                "partCode": "111",
                "invoiceId": 1,
                "id": 1
            },
            {
                "units": 5,
                "unitPrice": 15.0,
                "partCode": "222",
                "invoiceId": 1,
                "id": 2
            }
        ],
        "invoiceDate": "2020-08-27",
        "id": 1,
        "userId": 1
    }

..
