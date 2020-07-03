===============
Model Resources
===============

The design of the model resource configuration provides several areas to control the data provided via the request and the responses.

Class Variables
---------------

Set Up Variables
^^^^^^^^^^^^^^^^
Two variables are used for automatic URL generation with the function `get_urls()`. It is a convenience function. The url_prefix defaults to root, but can be set to as needed. The url_name is the name the resource and together they make up the URL.

It only comes in to play when adding resources.

* `url_prefix = '/'`
* `url_name = None`

If the url_name is left as None, a URL can be created from the model class name. For example, if a model class is `CustomerOrder` and its primary key is `id`, using a pluralizer, the default URLs will be:

.. code-block::

    /customer-orders
    /customer-orders/<int:id>

..

Date-Related Variables
^^^^^^^^^^^^^^^^^^^^^^
If your database does support automatic conversion of dates in string form, such as SQLite3, you can ask the ModelResource to do this:

* use_date_conversions = True

This variable defaults to False to avoid unnecessary processing, but it is helpful in the right situation.

Serialization
^^^^^^^^^^^^^

There are several avenues for controlling the output from model resources. Because the model classes use SQLAlchemy models wrapped with DBBase that have serialization / deserialization as a core process you can:

* Configure the Model Class serialization: This method would mean that the primary usage of DBBase model classes would be the same within the Flask environment or without as well.
* Configure the model resource class. This can be done by HTTP method or for all methods.

Model Resource Serial Fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Serial fields are the names of columns and other variables and functions as found in the Model classes. Serial field relations are the serial fields for related models as configured in relationships. For example, the author might be related via the book model.

The default for `serial_fields` and `serial_field_relations` looks like the following.

.. code-block:: python

    class MyResource(ModelResource):
        model_class = MyModel

        serial_fields = None
        serial_field_relations = None
..

The default serial fields and serial field relations uses what is found from the model class.

Here is an example where both the serial fields and serial field relations are specified. Note that `serial_field_relations` is a dict with keys for each relationship to be specified.

.. code-block:: python

    class MyResource(ModelResource):
        model_class = MyModel

        serial_fields = ["id", "field1", "field2", "field3"]
        serial_field_relations = {
            "RelatedModel1": ["id", "field1", "field2", "field3"],
            "RelatedModel2": ["id", "field1", "field2", "field3"],
        }
..

Here is an example where the serial fields and relations vary by method. At first, it might seem implausible that this would be ever necessary, but consider a model that is not complete unless it has been processed. The GET variables would return serial fields and relations for that model, but the POST, PUT, and PATCH methods would trigger a job. In that case, the serial fields and relations can be related to that job. Or, the default values for the Job model might be sufficient and that method could set as None. In this example, you would be using an `after_commit` process to create the job.

.. code-block:: python

    class MyResource(ModelResource):
        model_class = MyModel

        serial_fields = {
            "get": ["id", "field1", "field2", "field3"],
            "post": ["uuid", "job_name", "started_at"],
            "put": ["uuid", "job_name", "started_at"],
            "patch": ["uuid", "job_name", "started_at"],

        }

        serial_field_relations = {
            "get": {
                "RelatedModel1": ["id", "field1", "field2", "field3"],
                "RelatedModel2": ["id", "field1", "field2", "field3"],
            }
        }

..

.. include:: model-resource-modifications.rst
