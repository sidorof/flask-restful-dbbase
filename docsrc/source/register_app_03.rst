.. code-block:: bash 
    
    # meta info for register POST
    curl http://localhost:5000/meta/register/single?method=post \
        -H "Content-Type: application/json"
    
..

.. code-block:: json 

    {
        "method": {
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
                    "username": {
                        "type": "string",
                        "maxLength": 80,
                        "nullable": false,
                        "unique": true,
                        "info": {}
                    },
                    "email": {
                        "type": "string",
                        "maxLength": 80,
                        "nullable": false,
                        "unique": true,
                        "info": {}
                    },
                    "password": {
                        "type": "string",
                        "maxLength": 80,
                        "nullable": false,
                        "info": {
                            "writeOnly": true
                        }
                    },
                    "isStaff": {
                        "type": "boolean",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": false,
                            "is_clause_element": false,
                            "is_callable": false,
                            "is_scalar": true
                        },
                        "info": {}
                    },
                    "isActive": {
                        "type": "boolean",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": false,
                            "is_clause_element": false,
                            "is_callable": false,
                            "is_scalar": true
                        },
                        "info": {}
                    },
                    "isAccountCurrent": {
                        "type": "boolean",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": false,
                            "is_clause_element": false,
                            "is_callable": false,
                            "is_scalar": true
                        },
                        "info": {}
                    },
                    "dateJoined": {
                        "type": "date",
                        "nullable": true,
                        "default": {
                            "for_update": false,
                            "arg": "date.today",
                            "is_clause_element": false,
                            "is_callable": true,
                            "is_scalar": false
                        },
                        "info": {}
                    },
                    "lastLogin": {
                        "type": "date-time",
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
                        "username": {
                            "type": "string",
                            "maxLength": 80,
                            "nullable": false,
                            "unique": true,
                            "info": {}
                        },
                        "email": {
                            "type": "string",
                            "maxLength": 80,
                            "nullable": false,
                            "unique": true,
                            "info": {}
                        },
                        "password": {
                            "type": "string",
                            "maxLength": 80,
                            "nullable": false,
                            "info": {
                                "writeOnly": true
                            }
                        },
                        "is_staff": {
                            "type": "boolean",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": false,
                                "is_clause_element": false,
                                "is_callable": false,
                                "is_scalar": true
                            },
                            "info": {}
                        },
                        "is_active": {
                            "type": "boolean",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": false,
                                "is_clause_element": false,
                                "is_callable": false,
                                "is_scalar": true
                            },
                            "info": {}
                        },
                        "is_account_current": {
                            "type": "boolean",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": false,
                                "is_clause_element": false,
                                "is_callable": false,
                                "is_scalar": true
                            },
                            "info": {}
                        },
                        "date_joined": {
                            "type": "date",
                            "nullable": true,
                            "default": {
                                "for_update": false,
                                "arg": "date.today",
                                "is_clause_element": false,
                                "is_callable": true,
                                "is_scalar": false
                            },
                            "info": {}
                        },
                        "last_login": {
                            "type": "date-time",
                            "nullable": true,
                            "info": {}
                        }
                    }
                }
            }
        }
    }

..
