------------------------
Simple Owner App Revised
------------------------

We discussed how resources can be used to limit access by record as well as tables. Now we will look at customizing a resource to trigger an entry to a message queue within the context of simply saving a record.

In this example we will:

* modify our Order model slightly
* create a Job model
* create an example of an `after_commit()` function that will run just after committing the order to the database
* return the job details that has been created back to the frontend in place of the original order.

To keep the explanations short, we will focus on the changes made to the previous example.

As before, the code for this example is found in the examples section as

.. container:: default

    owner_app_v2 <https://github.com/sidorof/flask-restful-dbbase/blob/master/examples/owner_app_v2.py>
..


Models
------

The Order model will be used from the previous example with one change: It will maintain a relationship with the jobs that have been used to run whatever it is supposed to do.

.. include:: owner_app_v2_code_00.rst

The jobs column provides access to the jobs associated with an order.

And a Job model is created that will store the particulars of the job.

.. include:: owner_app_v2_code_01.rst


Order Resources
---------------
Now we recreate the order resources. To reflect the fact we are getting serious about the API and that it is the second version will add a url_prefix to the resources.

.. include:: owner_app_v2_code_02.rst

After Commit Function
---------------------

The `after_commit` is the key to this implementation. It runs just after the object has been commited to the database. In this case, we will use the order object as the basis for creating a job object, then pack the job off to a queue.

.. include:: owner_app_v2_code_03.rst

Revised Order Resource
----------------------
Our revised OrderResource is below:

.. include:: owner_app_v2_code_04.rst

You can see that the `after_commit` function that we created, `create_job` is associated with the POST and PUT methods. The other methods are unchanged by this process.

By default, the `serial_fields` and `serial_field_relations` will use the settings of the current object as the basis for returning data to the frontend. So, the GET and PATCH methods will automatically return Order data and POST and PUT will use the Job serial fields.

For no good reason, we will change the serial fields for Jobs to return only only the id, start time and status.

.. note::

    If you create an `after_commit` function that returns a different class than the one you with which you started, that new class must be added to the `serial_fields` class variable as we have done in the example. Otherwise, the meta resource has no way of knowing that you have made this choice. If you want to simply return the
    default serial fields for your replacement class then use the form such as:

    .. code-block:: python

        serial_fields = {
            "post": {Job: None},
            "put":  {Job: None},
        }
    ..

    which will guide the meta processes to select the right default values.


..

Job Resources
-------------

We can also monitor our jobs by creating Job resources.

.. include:: owner_app_v2_code_05.rst


With our revisions we will start again.

.. include:: owner_app_v2_code_06.rst


Use the API
-----------

Create an Order, Receive a Job
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v2_00.rst

We can see the serialized fields that we selected for a job.

Update an Order, Receive a Job
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v2_01.rst

Now we have run the same order a second time after updating the description.

Get Orders
^^^^^^^^^^
.. include:: owner_app_v2_02.rst

Notice that the full list of fields for the related jobs still shows. If we wanted to always show a restricted list of fields for jobs, the place to change that is upstream at the Job model by settinng its SERIAL_FIELDS.

Get Jobs
^^^^^^^^^

.. include:: owner_app_v2_03.rst


Order Meta Resource Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The meta information for the Order Resource is much the same as before. Lengthy as it is, the point of interest is found in the response variables for POST and PUT which shows the appropriate meta information for the Job serial fields selected.

.. include:: owner_app_v2_04.rst

Job Meta Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v2_05.rst

Next: :ref:`Parent Post - Child Records`
