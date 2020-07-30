.. code-block:: bash 
    
    # get an invoice
    curl http://localhost:5000/invoices/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "invoiceItems": [
            {
                "partCode": "111",
                "unitPrice": 20.0,
                "units": 1,
                "id": 1,
                "invoiceId": 1
            },
            {
                "partCode": "222",
                "unitPrice": 15.0,
                "units": 5,
                "id": 2,
                "invoiceId": 1
            }
        ],
        "invoiceDate": "2020-07-30",
        "userId": 1,
        "id": 1
    }

..
