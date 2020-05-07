Running Unit Tests
==================

Testing has been done for Sqlite3 and PostgreSQL.

There is a sample set of configs used for testing
at the root of this repo in the file `sample_configs.json`.
Change the variables as appropriate for your test environment.

A more complete sample file is `sample_configs_more.json` with
configuration for PostgreSQL.

.. code-block:: json

    [
        {
            "name": "postgresql",
            "testdb_uri": "postgresql://{user}:{password}@{host}:{port}/{dbname}",
            "testdb_vars": {
                "dbname": "testdb",
                "user": "suser",
                "password": "mypassword",
                "host": "localhost",
                "port": "5432",
                "basedb": "postgres"
            }
        },
        {
            "name": "sqlite_memory",
            "testdb_uri": ":memory:",
            "testdb_vars": {}
        },
        {
            "name": "sqlite_file",
            "testdb_uri": "sqlite:///{dbname}.db",
            "testdb_vars": {"dbname": "testdb"}
        }
    ]

..


Run the following command in the root of this repo:

.. code-block:: bash

    python3 -m unittest

..

Tests will be run for each configuration in `sample_configs.json`.
