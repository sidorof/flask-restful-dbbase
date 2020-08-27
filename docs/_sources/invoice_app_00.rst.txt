.. code-block:: bash 
    
    # post an invoice
    curl http://localhost:5000/invoices \
        -H "Content-Type: application/json" \
        -d '{
      "userId": 1,
      "invoiceDate": "2020-08-27",
      "invoiceItems": [
        {
          "partCode": "111",
          "units": "1",
          "unitPrice": 20.0
        },
        {
          "partCode": "222",
          "units": "5",
          "unitPrice": 15.0
        }
      ]
    }'
    
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
