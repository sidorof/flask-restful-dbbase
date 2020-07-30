.. code-block:: bash 
    
    # get documentation
    curl -g http://localhost:5000/meta/books/single
..

.. code-block:: JSON 

    {
        "modelClass": "Book",
        "urlPrefix": "/",
        "url": "/books",
        "methods": {
            "get": {
                "url": "/books/<int:id>",
                "requirements": [],
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
                        "pubYear": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "info": {}
                        },
                        "authorId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "author.id",
                            "info": {}
                        },
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "author": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Author",
                                "fields": {
                                    "id": {
                                        "type": "integer",
                                        "format": "int32",
                                        "primary_key": true,
                                        "nullable": true,
                                        "info": {}
                                    },
                                    "firstName": {
                                        "type": "string",
                                        "maxLength": 50,
                                        "nullable": false,
                                        "info": {}
                                    },
                                    "lastName": {
                                        "type": "string",
                                        "maxLength": 50,
                                        "nullable": false,
                                        "info": {}
                                    },
                                    "fullName": {
                                        "readOnly": true
                                    }
                                }
                            }
                        },
                        "title": {
                            "type": "string",
                            "maxLength": 100,
                            "nullable": false,
                            "info": {}
                        },
                        "isbn": {
                            "type": "string",
                            "maxLength": 20,
                            "nullable": true,
                            "info": {}
                        }
                    }
                }
            },
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
                    "isbn": {
                        "type": "string",
                        "maxLength": 20,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pubYear": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "authorId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "author.id",
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "pubYear": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "info": {}
                        },
                        "authorId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "author.id",
                            "info": {}
                        },
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "author": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Author",
                                "fields": {
                                    "id": {
                                        "type": "integer",
                                        "format": "int32",
                                        "primary_key": true,
                                        "nullable": true,
                                        "info": {}
                                    },
                                    "firstName": {
                                        "type": "string",
                                        "maxLength": 50,
                                        "nullable": false,
                                        "info": {}
                                    },
                                    "lastName": {
                                        "type": "string",
                                        "maxLength": 50,
                                        "nullable": false,
                                        "info": {}
                                    },
                                    "fullName": {
                                        "readOnly": true
                                    }
                                }
                            }
                        },
                        "title": {
                            "type": "string",
                            "maxLength": 100,
                            "nullable": false,
                            "info": {}
                        },
                        "isbn": {
                            "type": "string",
                            "maxLength": 20,
                            "nullable": true,
                            "info": {}
                        }
                    }
                }
            },
            "put": {
                "url": "/books/<int:id>",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "isbn": {
                        "type": "string",
                        "maxLength": 20,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pubYear": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "authorId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "author.id",
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "pubYear": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "info": {}
                        },
                        "authorId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "author.id",
                            "info": {}
                        },
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "author": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Author",
                                "fields": {
                                    "id": {
                                        "type": "integer",
                                        "format": "int32",
                                        "primary_key": true,
                                        "nullable": true,
                                        "info": {}
                                    },
                                    "firstName": {
                                        "type": "string",
                                        "maxLength": 50,
                                        "nullable": false,
                                        "info": {}
                                    },
                                    "lastName": {
                                        "type": "string",
                                        "maxLength": 50,
                                        "nullable": false,
                                        "info": {}
                                    },
                                    "fullName": {
                                        "readOnly": true
                                    }
                                }
                            }
                        },
                        "title": {
                            "type": "string",
                            "maxLength": 100,
                            "nullable": false,
                            "info": {}
                        },
                        "isbn": {
                            "type": "string",
                            "maxLength": 20,
                            "nullable": true,
                            "info": {}
                        }
                    }
                }
            },
            "patch": {
                "url": "/books/<int:id>",
                "requirements": [],
                "input": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "isbn": {
                        "type": "string",
                        "maxLength": 20,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pubYear": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "authorId": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "author.id",
                        "info": {}
                    }
                },
                "responses": {
                    "fields": {
                        "pubYear": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "info": {}
                        },
                        "authorId": {
                            "type": "integer",
                            "format": "int32",
                            "nullable": false,
                            "foreign_key": "author.id",
                            "info": {}
                        },
                        "id": {
                            "type": "integer",
                            "format": "int32",
                            "primary_key": true,
                            "nullable": true,
                            "info": {}
                        },
                        "author": {
                            "readOnly": true,
                            "relationship": {
                                "type": "single",
                                "entity": "Author",
                                "fields": {
                                    "id": {
                                        "type": "integer",
                                        "format": "int32",
                                        "primary_key": true,
                                        "nullable": true,
                                        "info": {}
                                    },
                                    "firstName": {
                                        "type": "string",
                                        "maxLength": 50,
                                        "nullable": false,
                                        "info": {}
                                    },
                                    "lastName": {
                                        "type": "string",
                                        "maxLength": 50,
                                        "nullable": false,
                                        "info": {}
                                    },
                                    "fullName": {
                                        "readOnly": true
                                    }
                                }
                            }
                        },
                        "title": {
                            "type": "string",
                            "maxLength": 100,
                            "nullable": false,
                            "info": {}
                        },
                        "isbn": {
                            "type": "string",
                            "maxLength": 20,
                            "nullable": true,
                            "info": {}
                        }
                    }
                }
            },
            "delete": {
                "url": "/books/<int:id>",
                "requirements": [],
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
            "Book": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "format": "int32",
                        "primary_key": true,
                        "nullable": true,
                        "info": {}
                    },
                    "isbn": {
                        "type": "string",
                        "maxLength": 20,
                        "nullable": true,
                        "info": {}
                    },
                    "title": {
                        "type": "string",
                        "maxLength": 100,
                        "nullable": false,
                        "info": {}
                    },
                    "pub_year": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "info": {}
                    },
                    "author_id": {
                        "type": "integer",
                        "format": "int32",
                        "nullable": false,
                        "foreign_key": "author.id",
                        "info": {}
                    },
                    "author": {
                        "readOnly": true,
                        "relationship": {
                            "type": "single",
                            "entity": "Author",
                            "fields": {
                                "id": {
                                    "type": "integer",
                                    "format": "int32",
                                    "primary_key": true,
                                    "nullable": true,
                                    "info": {}
                                },
                                "first_name": {
                                    "type": "string",
                                    "maxLength": 50,
                                    "nullable": false,
                                    "info": {}
                                },
                                "last_name": {
                                    "type": "string",
                                    "maxLength": 50,
                                    "nullable": false,
                                    "info": {}
                                },
                                "full_name": {
                                    "readOnly": true
                                }
                            }
                        }
                    }
                },
                "xml": "Book"
            }
        }
    }

..
