.. code-block:: bash 
    
    # post an invoice
    curl http://localhost:5000/invoices \
        -H "Content-Type: application/json" \
        -d '{
      "userId": 1,
      "invoiceDate": "2020-08-13",
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
