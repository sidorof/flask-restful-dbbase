.. code-block:: bash 
    
    # post an invoice
    curl http://localhost:5000/invoices \
        -H "Content-Type: application/json" \
        -d '{
      "userId": 1,
      "invoiceDate": "2020-07-29",
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
                "invoiceId": 1,
                "partCode": "111",
                "units": 1,
                "unitPrice": 20.0,
                "id": 1
            },
            {
                "invoiceId": 1,
                "partCode": "222",
                "units": 5,
                "unitPrice": 15.0,
                "id": 2
            }
        ],
        "userId": 1,
        "invoiceDate": "2020-07-29",
        "id": 1
    }

..
