Installation
============

To install the latest released version

.. code-block:: bash

   pip install dbbase
..

If you wish to install the latest development version, then use this:

.. code-block:: bash

   pip install git+https://github.com/sidorof/dbbase.git@master#egg=dbbase
..

Requirements
------------

* sqlalchemy
* your database driver, for example:

  * SQLite3: is already part of the python library
  * PostgreSQL: psycopg2 or psycopg2_binary

Note that since this is a fairly new project, unit testing has been done for Sqlite3 and PostgreSQL. More are expected to be added.
