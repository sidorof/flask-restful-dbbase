.. code-block:: bash 
    
    # get an invoice
    curl http://localhost:5000/invoices/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: json 

    {
        "id": 1,
        "userId": 1,
        "invoiceItems": [
            {
                "units": 1,
                "invoiceId": 1,
                "partCode": "111",
                "id": 1,
                "unitPrice": 20.0
            },
            {
                "units": 5,
                "invoiceId": 1,
                "partCode": "222",
                "id": 2,
                "unitPrice": 15.0
            }
        ],
        "invoiceDate": "2020-07-05"
    }

..
