.. code-block:: bash 
    
    # meta info for POST
    curl http://localhost:5000/meta/invoices/single?method=post \
        -H "Content-Type: application/json"
    
..

.. code-block:: JSON 

    {
        "modelClass": "Invoice",
        "urlPrefix": "/",
        "baseUrl": "/invoices",
        "methods": {
            "post": {
                "url": "/invoices",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "userId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "invoiceDate": {
                        "type": "date",
                        "nullable": false,
                        "info": {}
                    },
                    "invoiceItems": {
                        "readOnly": false,
                        "relationship": {
                            "type": "list",
                            "entity": "InvoiceItem",
                            "fields": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": true,
                                    "nullable": true,
                                    "info": {}
                                },
                                "invoiceId": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": false,
                                    "foreign_key": "invoice.id",
                                    "info": {}
                                },
                                "partCode": {
                                    "type": "string",
                                    "nullable": false,
                                    "info": {}
                                },
                                "units": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": false,
                                    "info": {}
                                },
                                "unitPrice": {
                                    "type": "float",
                                    "nullable": false,
                                    "info": {}
                                }
                            }
                        }
                    }
                },
                "responses": [
                    {
                        "fields": {
                            "invoiceItems": {
                                "readOnly": false,
                                "relationship": {
                                    "type": "list",
                                    "entity": "InvoiceItem",
                                    "fields": {
                                        "id": {
                                            "type": "integer",
                                            "format": "int32",
                                            "primary_key": true,
                                            "nullable": true,
                                            "info": {}
                                        },
                                        "invoiceId": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": false,
                                            "foreign_key": "invoice.id",
                                            "info": {}
                                        },
                                        "partCode": {
                                            "type": "string",
                                            "nullable": false,
                                            "info": {}
                                        },
                                        "units": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": false,
                                            "info": {}
                                        },
                                        "unitPrice": {
                                            "type": "float",
                                            "nullable": false,
                                            "info": {}
                                        }
                                    }
                                }
                            },
                            "invoiceDate": {
                                "type": "date",
                                "nullable": false,
                                "info": {}
                            },
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": true,
                                "nullable": true,
                                "info": {}
                            },
                            "userId": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": false,
                                "info": {}
                            }
                        }
                    }
                ]
            }
        },
        "table": {
            "Invoice": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "user_id": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "invoice_date": {
                        "type": "date",
                        "nullable": false,
                        "info": {}
                    },
                    "invoice_items": {
                        "readOnly": false,
                        "relationship": {
                            "type": "list",
                            "entity": "InvoiceItem",
                            "fields": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": true,
                                    "nullable": true,
                                    "info": {}
                                },
                                "invoice_id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": false,
                                    "foreign_key": "invoice.id",
                                    "info": {}
                                },
                                "part_code": {
                                    "type": "string",
                                    "nullable": false,
                                    "info": {}
                                },
                                "units": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": false,
                                    "info": {}
                                },
                                "unit_price": {
                                    "type": "float",
                                    "nullable": false,
                                    "info": {}
                                }
                            }
                        }
                    }
                },
                "xml": "Invoice"
            }
        }
    }

..
