.. code-block:: bash 
    
    # create an entry
    curl http://localhost:5000/meta/a-model-command/single \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "modelClass": "AModel",
        "urlPrefix": "/",
        "baseUrl": "/a-model-command",
        "methods": {
            "post": {
                "url": "/a-model-command",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "description": {
                        "type": "string",
                        "maxLength": 80,
                        "nullable": false,
                        "unique": true,
                        "info": {}
                    },
                    "numVariable": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    }
                },
                "after_commit": "Here we can say a few words about the process",
                "responses": [
                    {
                        "messsage": "Here we can describe the response"
                    }
                ]
            }
        },
        "table": {
            "AModel": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "description": {
                        "type": "string",
                        "maxLength": 80,
                        "nullable": false,
                        "unique": true,
                        "info": {}
                    },
                    "num_variable": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    }
                },
                "xml": "AModel"
            }
        }
    }

..
