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

Additional Variable

* `max_page_size` = None

`max_page_size` can be used automatically limit the number of entries in a list for paging to avoid outputting too much in one query.


Input Processing
^^^^^^^^^^^^^^^^

The following parameters and returns should be used for `process_get_input`.

+----------------+----------------------------------+----------------------------------+
|                | Args                             |  Returns a tuple                 |
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

.. note::
    This package is under active development and more query options will become available soon.

Within the query string there can also be other variables:

* `page_size`: This limits the number entries that are output.If the page size is greater than max_page_size, then the max_page_size will be used instead.
* `offset`: This is the number of entries to skip before outputting lines
* `debug`: If True, it will return the SQL query instead of executing to help assess if it is formulated correctly.
* `order_by`: This is the order of the list and multiple variables can be used.

Note that the parameter variables can enter as camel case and will be converted along with the column names and variables.

Processing the Query
^^^^^^^^^^^^^^^^^^^^
Once the query has been processed, the serial fields and relational fields will be applied to create the output. The form of the out is:

.. code-block:: json

    {"MyModel": [
        {"id": 1, "field1": value1, "field2": value2, ...},
        {"id": 2, "field1": value1, "field2": value2, ...},
        {"id": 3, "field1": value1, "field2": value2, ...},
        {"id": 4, "field1": value1, "field2": value2, ...}
    ]}

..
