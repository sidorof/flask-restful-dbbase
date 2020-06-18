============================
Model Resource Modifications
============================

Model resources can cover a fair amount of ground for a datacentric
API, but when the vanilla version will not fit, there are remedies
as a fall-back solution rather than simply writing your own.

Model resources are preset to take functions that can insert your
necessary logic into the right point in the processing cycle.

There are three insertion points. The details change, depending upon the HTTP method, but there are more similarities than differences.

* `Process Input Functions`_: Modify the input data, and continue processing or close it out early.
* `Adjustments Before or After Commits`_
    * Before Commit: Just prior to a commit, either a function or class can be inserted. This gives the possibility of a rollback of the session or diversion to other process.
    * After Commit: After a commit, either a function or class can be inserted. This can then be a trigger process or complete substitution of another class for the return trip.

Process Input Functions
-----------------------

Process input functions take the form of a function that can
process the input data for the HTTP methods.

The format name for these functions is `process_{method}_input`.

Since HTTP methods have different requirements for input data,
the inputs vary according to the method. And, since these
functions are inserted into an on-going process, there are certain
requirements.


Input Variables
+++++++++++++++
* `kwargs`: as passed into the method
* `data`: the data gleaned from the request in a dictionary form: This is the data prior to deserializations, so the variable names would be in camel case still.
* `query`: the SQLAlchemy query that can be modified: This the Flask-SQLAlchemy version of query, equivalent to the SQLAlchemy's session.query(Model), for example `session.query(Book)`. So an additional filter as may be necessary would be done by `query = query.filter_by(my_var='test')`. And finally, this is an unexecuted query that the normal program will execute afterwards.

Returns
+++++++
Since part of the point of these functions is to determine whether to go forward or not, the returns must be in the form `(status, result)` where status is either `True` to contine or `False` to exit early. So, if a tuple is not returned an error will be returned.

Use the following formats as a guide.

process_get_input
^^^^^^^^^^^^^^^^^
.. code-block:: python

    def process_get_input(self, query, kwargs):

        # your code runs

        # if success
        return (True, query)

        # if exit
        return False, ({"message": "an explanation"}, status_code)

..

process_post_input
^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def process_post_input(self, query):

        # your code runs

        # if success
        return (True, query)

        # if exit
        return False, ({"message": "an explanation"}, status_code)

..


process_put_input
^^^^^^^^^^^^^^^^^
.. code-block:: python

    def process_post_input(self, query, data, kwargs):

        # your code runs

        # if success
        return (True, (query, data))

        # if exit
        return False, ({"message": "an explanation"}, status_code)

..


process_patch_input
^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def process_patch_input(self, query, data, kwargs):

        # your code runs

        # if success
        return (True, (query, data))

        # if exit
        return False, ({"message": "an explanation"}, status_code)

..


process_delete_input
^^^^^^^^^^^^^^^^^^^^
.. code-block:: python

    def process_delete_input(self, query, kwargs):

        # your code runs

        # if success
        return (True, query)

        # if exit
        return False, ({"message": "an explanation"}, status_code)

..


Adjustments Before or After Commits
-----------------------------------

Being able to jump in prior to a commit or just after can be very helpful. Possible areas:

* Triggering another process to run instead of saving, or run directly after saving.
* A record could be marked as inactive rather than deleted.
* A separate job could be created and sent to a queue, the job object returned in place of the original record.

The process inputs all had separate names and the input and return variables varied with the HTTP method, while this family of functions are more similiar.

To make the interface a little cleaner a ModelResource before / after commit is organized as a dict. For example:

.. code-block:: python

    MachineLearningModelResource(ModelResource):
        model_class = MachineLearningModel

        after_commit = {
            "post": submit_job
            "put": submit_job1
        }

..

So your `submit_job` function would be called on POST or PUT, otherwise not.

The format of the before / after functions is similar to the following:

.. code-block:: python


    def my_before_commit(self, item, status_code):
        """
        This function could be before or after, the params are the
        same.

        Args:
            item: (obj): This is the data model record
            status_code: (int) : This will be the default response
            status code for this method. If it turns out that a
            different status code makes more sense, it can be
            changed on the return.

        Returns:
            item: (obj) : The object that will be returned. Note that
            it does not have to be the same object that entered. As
            long as it is DBBase model, the serialization will use the
            serialization meant the current object.

            status_code: (int) : This would be just passthrough of the
            default status code, but it could be changed to a 202, for
            example if it is starting a job.

        """

        # your code runs

        return item, status_code

..



