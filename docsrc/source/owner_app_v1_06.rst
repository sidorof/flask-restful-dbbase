.. code-block:: bash 
    
    # get meta data for OrderResource
    curl http://localhost:5000/meta/orders/single \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1"
    
..

.. code-block:: JSON 

    {
        "modelClass": "Order",
        "urlPrefix": "/",
        "url": "/orders",
        "methods": {
            "get": {
                "url": "/orders/<int:id>",
                "requirements": [
                    "mock_jwt_required"
                ],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "orderedAt": {
                            "type": "date-time",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": "datetime.now",
                                "is_clause_element": false,
                                "is_callable": true,
                                "is_scalar": false
                            },
                            "info": {}
                        },
                        "description": {
                            "type": "string",
                            "nullable": false,
                            "info": {}
                        },
                        "statusId": {
                            "type": "integer",
                            "format": "int8",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": 0,
                                "is_clause_element": false,
                                "is_callable": false,
                                "is_scalar": true
                            },
                            "info": {}
                        },
                        "ownerId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "user.id",
                            "info": {}
                        }
                    }
                }
            },
            "post": {
                "requirements": [
                    "mock_jwt_required"
                ],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "ownerId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "user.id",
                        "info": {}
                    },
                    "description": {
                        "type": "string",
                        "nullable": false,
                        "info": {}
                    },
                    "orderedAt": {
                        "type": "date-time",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": "datetime.now",
                            "is_clause_element": false,
                            "is_callable": true,
                            "is_scalar": false
                        },
                        "info": {}
                    },
                    "statusId": {
                        "type": "integer",
                        "format": "int8",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": 0,
                            "is_clause_element": false,
                            "is_callable": false,
                            "is_scalar": true
                        },
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "orderedAt": {
                            "type": "date-time",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": "datetime.now",
                                "is_clause_element": false,
                                "is_callable": true,
                                "is_scalar": false
                            },
                            "info": {}
                        },
                        "description": {
                            "type": "string",
                            "nullable": false,
                            "info": {}
                        },
                        "statusId": {
                            "type": "integer",
                            "format": "int8",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": 0,
                                "is_clause_element": false,
                                "is_callable": false,
                                "is_scalar": true
                            },
                            "info": {}
                        },
                        "ownerId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "user.id",
                            "info": {}
                        }
                    }
                }
            },
            "put": {
                "url": "/orders/<int:id>",
                "requirements": [
                    "mock_jwt_required"
                ],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "ownerId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "user.id",
                        "info": {}
                    },
                    "description": {
                        "type": "string",
                        "nullable": false,
                        "info": {}
                    },
                    "orderedAt": {
                        "type": "date-time",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": "datetime.now",
                            "is_clause_element": false,
                            "is_callable": true,
                            "is_scalar": false
                        },
                        "info": {}
                    },
                    "statusId": {
                        "type": "integer",
                        "format": "int8",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": 0,
                            "is_clause_element": false,
                            "is_callable": false,
                            "is_scalar": true
                        },
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "orderedAt": {
                            "type": "date-time",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": "datetime.now",
                                "is_clause_element": false,
                                "is_callable": true,
                                "is_scalar": false
                            },
                            "info": {}
                        },
                        "description": {
                            "type": "string",
                            "nullable": false,
                            "info": {}
                        },
                        "statusId": {
                            "type": "integer",
                            "format": "int8",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": 0,
                                "is_clause_element": false,
                                "is_callable": false,
                                "is_scalar": true
                            },
                            "info": {}
                        },
                        "ownerId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "user.id",
                            "info": {}
                        }
                    }
                }
            },
            "patch": {
                "url": "/orders/<int:id>",
                "requirements": [
                    "mock_jwt_required"
                ],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "ownerId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "user.id",
                        "info": {}
                    },
                    "description": {
                        "type": "string",
                        "nullable": false,
                        "info": {}
                    },
                    "orderedAt": {
                        "type": "date-time",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": "datetime.now",
                            "is_clause_element": false,
                            "is_callable": true,
                            "is_scalar": false
                        },
                        "info": {}
                    },
                    "statusId": {
                        "type": "integer",
                        "format": "int8",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": 0,
                            "is_clause_element": false,
                            "is_callable": false,
                            "is_scalar": true
                        },
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "orderedAt": {
                            "type": "date-time",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": "datetime.now",
                                "is_clause_element": false,
                                "is_callable": true,
                                "is_scalar": false
                            },
                            "info": {}
                        },
                        "description": {
                            "type": "string",
                            "nullable": false,
                            "info": {}
                        },
                        "statusId": {
                            "type": "integer",
                            "format": "int8",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": 0,
                                "is_clause_element": false,
                                "is_callable": false,
                                "is_scalar": true
                            },
                            "info": {}
                        },
                        "ownerId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "user.id",
                            "info": {}
                        }
                    }
                }
            },
            "delete": {
                "url": "/orders/<int:id>",
                "requirements": [
                    "mock_jwt_required"
                ],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    }
                },
                "responses": {}
            }
        },
        "table": {
            "Order": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "owner_id": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "user.id",
                        "info": {}
                    },
                    "description": {
                        "type": "string",
                        "nullable": false,
                        "info": {}
                    },
                    "ordered_at": {
                        "type": "date-time",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": "datetime.now",
                            "is_clause_element": false,
                            "is_callable": true,
                            "is_scalar": false
                        },
                        "info": {}
                    },
                    "status_id": {
                        "type": "integer",
                        "format": "int8",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": 0,
                            "is_clause_element": false,
                            "is_callable": false,
                            "is_scalar": true
                        },
                        "info": {}
                    }
                },
                "xml": "Order"
            }
        }
    }

..
