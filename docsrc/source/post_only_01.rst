.. code-block:: bash 
    
    # create an entry
    curl http://localhost:5000/meta/a-model-command/single \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "modelClass": "AModel",
        "urlPrefix": "/",
        "url": "/a-model-command",
        "methods": {
            "post": {
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
                "afterCommit": "This now returns a custom message"
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
