.. code-block:: bash 
    
    # get meta data for OrderResource
    curl http://localhost:5000/api/v2/meta/orders/single \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1"
    
..

.. code-block:: JSON 

    {
        "modelClass": "Order",
        "urlPrefix": "/api/v2",
        "baseUrl": "/api/v2/orders",
        "methods": {
            "get": {
                "url": "/api/v2/orders/<int:id>",
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    }
                },
                "responses": [
                    {
                        "fields": {
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
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": true,
                                "nullable": true,
                                "info": {}
                            },
                            "jobs": {
                                "readOnly": false,
                                "relationship": {
                                    "type": "list",
                                    "entity": "Job",
                                    "fields": {
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
                                        "orderId": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": false,
                                            "foreign_key": "order.id",
                                            "info": {}
                                        },
                                        "startedAt": {
                                            "type": "date-time",
                                            "nullable": false,
                                            "server_default": {
                                                "for_update": false,
                                                "arg": "db.func.now()",
                                                "reflected": false
                                            },
                                            "info": {}
                                        },
                                        "finishedAt": {
                                            "type": "date-time",
                                            "nullable": true,
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
                                    }
                                }
                            },
                            "ownerId": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": false,
                                "foreign_key": "user.id",
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
                            }
                        }
                    }
                ]
            },
            "post": {
                "url": "/api/v2/orders",
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
                    },
                    "jobs": {
                        "readOnly": false,
                        "relationship": {
                            "type": "list",
                            "entity": "Job",
                            "fields": {
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
                                "orderId": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": false,
                                    "foreign_key": "order.id",
                                    "info": {}
                                },
                                "startedAt": {
                                    "type": "date-time",
                                    "nullable": false,
                                    "server_default": {
                                        "for_update": false,
                                        "arg": "db.func.now()",
                                        "reflected": false
                                    },
                                    "info": {}
                                },
                                "finishedAt": {
                                    "type": "date-time",
                                    "nullable": true,
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
                            }
                        }
                    }
                },
                "responses": [
                    {
                        "fields": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": true,
                                "nullable": true,
                                "info": {}
                            },
                            "startedAt": {
                                "type": "date-time",
                                "nullable": false,
                                "server_default": {
                                    "for_update": false,
                                    "arg": "db.func.now()",
                                    "reflected": false
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
                        }
                    }
                ]
            },
            "put": {
                "url": "/api/v2/orders/<int:id>",
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
                    },
                    "jobs": {
                        "readOnly": false,
                        "relationship": {
                            "type": "list",
                            "entity": "Job",
                            "fields": {
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
                                "orderId": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": false,
                                    "foreign_key": "order.id",
                                    "info": {}
                                },
                                "startedAt": {
                                    "type": "date-time",
                                    "nullable": false,
                                    "server_default": {
                                        "for_update": false,
                                        "arg": "db.func.now()",
                                        "reflected": false
                                    },
                                    "info": {}
                                },
                                "finishedAt": {
                                    "type": "date-time",
                                    "nullable": true,
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
                            }
                        }
                    }
                },
                "responses": [
                    {
                        "fields": {
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": true,
                                "nullable": true,
                                "info": {}
                            },
                            "startedAt": {
                                "type": "date-time",
                                "nullable": false,
                                "server_default": {
                                    "for_update": false,
                                    "arg": "db.func.now()",
                                    "reflected": false
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
                        }
                    }
                ]
            },
            "patch": {
                "url": "/api/v2/orders/<int:id>",
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
                    },
                    "jobs": {
                        "readOnly": false,
                        "relationship": {
                            "type": "list",
                            "entity": "Job",
                            "fields": {
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
                                "orderId": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": false,
                                    "foreign_key": "order.id",
                                    "info": {}
                                },
                                "startedAt": {
                                    "type": "date-time",
                                    "nullable": false,
                                    "server_default": {
                                        "for_update": false,
                                        "arg": "db.func.now()",
                                        "reflected": false
                                    },
                                    "info": {}
                                },
                                "finishedAt": {
                                    "type": "date-time",
                                    "nullable": true,
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
                            }
                        }
                    }
                },
                "responses": [
                    {
                        "fields": {
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
                            "id": {
                                "type": "integer",
                                "format": "int32",
                                "primary_key": true,
                                "nullable": true,
                                "info": {}
                            },
                            "jobs": {
                                "readOnly": false,
                                "relationship": {
                                    "type": "list",
                                    "entity": "Job",
                                    "fields": {
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
                                        "orderId": {
                                            "type": "integer",
                                            "format": "int32",
                                            "nullable": false,
                                            "foreign_key": "order.id",
                                            "info": {}
                                        },
                                        "startedAt": {
                                            "type": "date-time",
                                            "nullable": false,
                                            "server_default": {
                                                "for_update": false,
                                                "arg": "db.func.now()",
                                                "reflected": false
                                            },
                                            "info": {}
                                        },
                                        "finishedAt": {
                                            "type": "date-time",
                                            "nullable": true,
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
                                    }
                                }
                            },
                            "ownerId": {
                                "type": "integer",
                                "format": "int32",
                                "nullable": false,
                                "foreign_key": "user.id",
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
                            }
                        }
                    }
                ]
            },
            "delete": {
                "url": "/api/v2/orders/<int:id>",
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    }
                },
                "responses": [
                    {}
                ]
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
                    },
                    "jobs": {
                        "readOnly": false,
                        "relationship": {
                            "type": "list",
                            "entity": "Job",
                            "fields": {
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
                                "order_id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "nullable": false,
                                    "foreign_key": "order.id",
                                    "info": {}
                                },
                                "started_at": {
                                    "type": "date-time",
                                    "nullable": false,
                                    "server_default": {
                                        "for_update": false,
                                        "arg": "db.func.now()",
                                        "reflected": false
                                    },
                                    "info": {}
                                },
                                "finished_at": {
                                    "type": "date-time",
                                    "nullable": true,
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
                            }
                        }
                    }
                },
                "xml": "Order"
            }
        }
    }

..
