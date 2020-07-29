.. code-block:: bash 
    
    # get an invoice
    curl http://localhost:5000/invoices/1 \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "userId": 1,
        "id": 1,
        "invoiceItems": [
            {
                "id": 1,
                "units": 1,
                "unitPrice": 20.0,
                "invoiceId": 1,
                "partCode": "111"
            },
            {
                "id": 2,
                "units": 5,
                "unitPrice": 15.0,
                "invoiceId": 1,
                "partCode": "222"
            }
        ],
        "invoiceDate": "2020-07-29"
    }

..
