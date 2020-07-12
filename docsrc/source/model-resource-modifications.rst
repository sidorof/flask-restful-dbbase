Model Resource Modifications
----------------------------

Model resources can cover a fair amount of ground for a datacentric API, but when the vanilla version will not fit, there are remedies as a fall-back solution rather than simply writing your own.

Model resources are preset to take functions that can insert your necessary logic into the right point in the processing cycle.

There are three insertion points. The details change, depending upon the HTTP method, but there are more similarities than differences.

* `Process Input Functions`_: Modify the input data or query and continue processing or close it out early.
* `Adjustments Before or After Commits`_
    * Before Commit: Just prior to a commit, either a function or class can be inserted. This gives the possibility of a rollback of the session or diversion to another process.
    * After Commit: After a commit, either a function or class can be inserted. This can then be a trigger process or complete substitution of another class for the return trip.

Process Input Functions
^^^^^^^^^^^^^^^^^^^^^^^

Process input functions take the form of a function that can
process the input data for the HTTP methods.

The format template for these functions is `process_{method}_input`.

Since HTTP methods have different requirements for input data, the inputs vary according to the method. And, since these functions are inserted into an on-going process, the arguments and returns for the functions are specific. However, the returns follow a common format of `(status, result)`. The status is a True / False indicating that you would like the method to continue with the possibly altered data. `False` indicates that the method should end. A failure must have a tuple of a text message and a response status code that will be made into a return result and returned to the front end.

Input Variables
+++++++++++++++
* `kwargs`: as passed into the method
* `data`: the data gleaned from the request in a dictionary form: This is the data prior to deserializations, so the variable names would be in camel case still.
* `query`: the SQLAlchemy query that can be modified: This is the Flask-SQLAlchemy version of query, equivalent to the SQLAlchemy's session.query(Model), for example `session.query(Book)`. So an additional filter as may be necessary would be done by

.. code-block:: python

    query = query.filter_by(my_var='test').

..

And finally, this is an unexecuted query that the normal program will execute afterwards.

Returns
+++++++
Since part of the point of these functions is to determine whether to go forward or not, the returns must be in the form `(status, result)` where status is either `True` to continue or `False` to exit early. So, if a tuple is not returned an error will be triggered about the process_input_function itself.

Use the following formats as a guide.

+----------------+----------------------------------+----------------------------------+
|                | Args                             |  Returns a tuple                 |
|                +------+-------+--------+----------+---------+------------------------+
| Method         | self | query |  data  |  kwargs  |  status |   result               |
+----------------+------+-------+--------+----------+---------+------------------------+
| GET            |  X   |  X    |   X    |   X      |   True  | (query, data)          |
|                |      |       |        |          +---------+------------------------+
|                |      |       |        |          |   False | (message, status_code) |
+----------------+------+-------+--------+----------+---------+------------------------+
| POST           |  X   |       |   X    |          |   True  | data                   |
|                |      |       |        |          +---------+------------------------+
|                |      |       |        |          |   False | (message, status_code) |
+----------------+------+-------+--------+----------+---------+------------------------+
| PUT            |  X   |  X    |   X    |   X      |   True  | (query, data)          |
|                |      |       |        |          +---------+------------------------+
|                |      |       |        |          |   False | (message, status_code) |
+----------------+------+-------+--------+----------+---------+------------------------+
| PATCH          |  X   |  X    |   X    |   X      |   True  | (query, data)          |
|                |      |       |        |          +---------+------------------------+
|                |      |       |        |          |   False | (message, status_code) |
+----------------+------+-------+--------+----------+---------+------------------------+
| DELETE         |  X   |       |        |   X      |   True  | query                  |
|                |      |       |        |          +---------+------------------------+
|                |      |       |        |          |   False | (message, status_code) |
+----------------+------+-------+--------+----------+---------+------------------------+

For example, suppose you want to add a process input function for POST.

.. code-block:: python

    class MyResource(ModelResource):
        model_class = MyClass

        def process_post_input(self, data):
            # your magic here
            return status, result

..


Adjustments Before or After Commits
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Being able to jump in prior to a commit or just after can be very helpful. Possible areas:

* Triggering another process to run instead of saving, or run directly after saving.
* A record could be marked as inactive rather than deleted.
* A separate job could be created and sent to a queue, the job object returned in place of the original record.
* A process can be run which diverts to an exit of the HTTP method with a message and status code.


The process inputs all had separate names and the input and return variables varied with the HTTP method, while this family of functions are more similar.

These functions must return a status of True to continue to output a data item after adjustments. If a status of False is used, the process will exit the HTTP method with a message and a status code.

.. note::

    By diverting the process to return a message and status code, it is now essentially an RPC.

..

To make the interface a little cleaner a ModelResource before / after commit is organized as a dict. For example:

.. code-block:: python

    MachineLearningModelResource(ModelResource):
        model_class = MachineLearningModel

        after_commit = {
            "post": submit_job
            "put": submit_job
        }

..

So your `submit_job` function would be called on POST or PUT, otherwise not.

The format of the before / after functions is similar to the following:

+----------------+-----------------------------------------------------+-------------------------------+
|                | Args                                                |  Returns a tuple              |
|                |                                                     +-------------------------------+
| Method         |                                                     |  status, result, status_code  |
+----------------+------+----------------+-------------+---------------+-------------------------------+
| before_commit  | self |  your_function |  data item  |  status_code  |   True, item, status_code     |
| after_commit   |      |                |             |               +-------------------------------+
|                |      |                |             |               |   False, message, status_code |
+----------------+------+----------------+-------------+---------------+-------------------------------+




