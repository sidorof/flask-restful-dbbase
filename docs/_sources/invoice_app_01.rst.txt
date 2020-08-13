.. code-block:: bash 
    
    # get an invoice
    curl http://localhost:5000/invoices/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "userId": 1,
        "invoiceDate": "2020-08-13",
        "id": 1,
        "invoiceItems": [
            {
                "units": 1,
                "id": 1,
                "invoiceId": 1,
                "unitPrice": 20.0,
                "partCode": "111"
            },
            {
                "units": 5,
                "id": 2,
                "invoiceId": 1,
                "unitPrice": 15.0,
                "partCode": "222"
            }
        ]
    }

..
