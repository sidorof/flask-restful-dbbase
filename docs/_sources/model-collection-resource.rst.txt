==========================
Model Collection Resources
==========================

Model collection resources are configured for HTTP GET methods only to conform to common usage patterns.

* the default URL function returns a single URL, such as [`/api/v1/items`]. Note that it is still wrapped in a list for consistency for usage in
    `api.add_resource(MyCollection, *MyCollection.get_urls())`
* serialization / deserialization services operate in the same fashion as the ModelResource class.
* `process_get_input` is the same except that kwargs are not used.
* Additional class variables are used to assist in returning lists.
* the parser for the `query_string` looks for additional variables to provide guidance for the database queries such as sorting, filtering, paging.


Class Variables
^^^^^^^^^^^^^^^

As discussed in :ref:`Model Resources` class variables are used here as well.

* `url_prefix`
* `url_name`
* `serial_fields`
* `serial_field_relations`
* `process_get_input`

Additional Variable Defaults

* `max_page_size` = None
* `order_by` = None


`max_page_size` can be used automatically limit the number of entries in a list for paging to avoid outputting too much in one query.


Input Processing
^^^^^^^^^^^^^^^^

The following parameters and returns should be used for `process_get_input`. Like the model resource, the function must return a dictionary in the format of:

.. code-block:: python

    {"status" True, "query": query, "data": data}
    {"status": False, "message": message, "status_code": status_code}

..

A status of True enables normal processing, but with some tweaking of the data or query for this particular resource.

A status of False diverts normal processing to abort the process or send it in another direction.


+----------------+----------------------------------+----------------------------------+
|                | Args                             |  Returns a dictionary                 |
|                +------+-------+--------+----------+---------+------------------------+
| Method         | self | query |  data  |  kwargs  |  status |   result               |
+----------------+------+-------+--------+----------+---------+------------------------+
| GET            |  X   |  X    |   X    |          |   True  | (query, data)          |
|                |      |       |        |          +---------+------------------------+
|                |      |       |        |          |   False | (message, status_code) |
+----------------+------+-------+--------+----------+---------+------------------------+


Queries
^^^^^^^

The GET method looks to the `request.query_string` for filtering the resource, using a dict of
column names as keys and specific values for which to select.

The standard format for the query string:

.. code-block:: python

    query_string = {"var1": val1}

..

Select multiple values from the same variable:

.. code-block:: python

    query_string = {"var2[]": [val1, val2, val3, ...]}

..

Comparison operators for a single value can also be used:

.. code-block:: python

    query_string = {"var3": [operator, val1 ]}

..

The operator must be found in `["eq", "ne", "gt", "ge", "lt", "le", "like", "ilike", "notlike", "notilike"]`.


Variables can also be filtered by comparing to other variables. Putting a prefix of `var:` alerts the selection to use a column name.

.. code-block:: python

    query_string = {"var5": ["gt", "var:var6"]}

..

Within the query string there can also be other variables. To avoid cluttering up column name space, these variables are behind the keyword, `page_config`.

.. code-block:: python

    query_string = {
        "var1": val1,
        "page_config": {
            "order_by": var1
        }
    }

..

* `page_size`: This limits the number entries that are output.If the page size is greater than a class resource variable, `max_page_size`, then the max_page_size will be used instead.
* `offset`: This is the number of entries to skip before outputting lines
* `order_by`: This is the order of the list and multiple variables can be used.
.. code-block:: python

    Examples:

    "order_by": "var1"      ascending
    "order_by": "-var1"     descending

    "order_by": ["var1", "var2"]

..

* `serial_fields`: Control of the fields returned can controlled by query. This enables a query to limit the number of fields by query. The default fields derive from the underlying `DBBase` model. Within the model the fields can be specified. Also, the resource model can also define what fields are returned. So, multiple levels of detail can be returned, depending upon the application.

* `debug`: If True, it will return the SQL query and other information instead of executing the query to help assess if it is formulated correctly.


Note that the parameter variables can enter as camel case and will be converted along with the column names and variables.

Processing the Query
^^^^^^^^^^^^^^^^^^^^
Once the query has been processed, the serial fields and relational fields will be applied to create the output. The form of the output is:


.. code-block:: json


    {"MyModel": [
        {"id": 1, "field1": value1, "field2": value2, ...},
        {"id": 2, "field1": value1, "field2": value2, ...},
        {"id": 3, "field1": value1, "field2": value2, ...},
        {"id": 4, "field1": value1, "field2": value2, ...}
    ]}

..

Next: :ref:`Meta Resources`
