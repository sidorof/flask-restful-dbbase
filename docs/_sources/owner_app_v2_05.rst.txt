.. code-block:: bash 
    
    # get meta data for JobResource
    curl http://localhost:5000/api/v2/meta/jobs/single \
        -H "Content-Type: application/json" \
        -H "Authorization: User:1"
    
..

.. code-block:: JSON 

    {
        "modelClass": "Job",
        "urlPrefix": "/api/v2",
        "url": "/api/v2/jobs",
        "methods": {
            "get": {
                "url": "/api/v2/jobs/<int:id>",
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
                        "orderId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "order.id",
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
                        "order": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Order",
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
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
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
                },
                "responses": {
                    "fields": {
                        "orderId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "order.id",
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
                        "order": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Order",
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
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        }
                    }
                }
            },
            "put": {
                "url": "/api/v2/jobs/<int:id>",
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
                },
                "responses": {
                    "fields": {
                        "orderId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "order.id",
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
                        "order": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Order",
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
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        }
                    }
                }
            },
            "patch": {
                "url": "/api/v2/jobs/<int:id>",
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
                },
                "responses": {
                    "fields": {
                        "orderId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "order.id",
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
                        "order": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Order",
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
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        }
                    }
                }
            },
            "delete": {
                "url": "/api/v2/jobs/<int:id>",
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
            "Job": {
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
                    },
                    "order": {
                        "readOnly": true,
                        "relationship": {
                            "type": "single",
                            "entity": "Order",
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
                            }
                        }
                    }
                },
                "xml": "Job"
            }
        }
    }

..
