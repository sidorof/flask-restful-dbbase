.. code-block:: bash 
    
    # post an invoice
    curl http://localhost:5000/invoices \
        -H "Content-Type: application/json" \
        -d '{
      "userId": 1,
      "invoiceDate": "2020-07-30",
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
