.. code-block:: bash 
    
    # get an invoice
    curl http://localhost:5000/invoices/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: json 

    {
        "userId": 1,
        "invoiceDate": "2020-07-02",
        "invoiceItems": [
            {
                "invoiceId": 1,
                "partCode": "111",
                "units": 1,
                "id": 1,
                "unitPrice": 20.0
            },
            {
                "invoiceId": 1,
                "partCode": "222",
                "units": 5,
                "id": 2,
                "unitPrice": 15.0
            }
        ],
        "id": 1
    }

..
