.. code-block:: bash 
    
    # post an invoice
    curl http://localhost:5000/invoices \
        -H "Content-Type: application/json" \
        -d '{
      "userId": 1,
      "invoiceDate": "2020-07-05",
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
