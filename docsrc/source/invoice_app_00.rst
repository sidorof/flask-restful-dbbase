.. code-block:: bash 
    
    # post an invoice
    curl http://localhost:5000/invoices \
        -H "Content-Type: application/json" \
        -d '{
      "userId": 1,
      "invoiceDate": "2020-07-02",
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
        "userId": 1,
        "invoiceDate": "2020-07-02",
        "invoiceItems": [
            {
                "invoiceId": 2,
                "partCode": "111",
                "units": 1,
                "id": 3,
                "unitPrice": 20.0
            },
            {
                "invoiceId": 2,
                "partCode": "222",
                "units": 5,
                "id": 4,
                "unitPrice": 15.0
            }
        ],
        "id": 2
    }

..
