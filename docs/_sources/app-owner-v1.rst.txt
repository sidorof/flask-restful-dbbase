----------------------
Simple Owner App
----------------------

We discussed how resources use the table models as the basis for validating incoming data, and presentation of return data. Now we will look at how additional capabilities can be be brought to bear.

To get a better understanding of why these capabilities matter, let us look at a few scenarios and see how they can be solved by taking some additional actions.

We touched on how access to data can be limited to authenticated users by table using method decorators, a feature that is part of Flask-RESTful. But suppose we want to let users only see information related to their own accounts? That would mean that we need to restrict on a record by record basis, not the table or method.

This would be time to write some code for that method that gets the authenticated `user_id`, does some checking and passes it along, or not. But then, you would need to write the rest of the code for that method.

We will still write some code, but by inserting it in the right place there should be less of it.

The :class:`~flask_restful_dbbase.resources.ModelResource` class by design contains places to alter the flow. For example, the following modifications can be made to the POST process.

- Can append an additional filter to a query, or replace it entirely.
- After validation, a data record is created, an additional modification can be made just prior to a commit.
- After a commit, actions can be taken.

The last two options can also be used to submit jobs to queues and return a job object instead, whatever else fits the situation.

Owner Based Tables
------------------
This description has been somewhat abstract, so we will now create a simplified example to show possible modifications to the process in a concrete way.

We will control

- who sees what
- altering the flow of processing
- changing the response returned to the user


As before the code for this example is found in the examples section as

.. container:: default

    owner_app_v1 <https://sidorof.github.io/flask-restful-dbbase/examples/owner_app_v1.py>
..

Initiate the App and Models
---------------------------

To implement this example, we will create two tables:

- A user table
- An order table, that is apparently a request for a service.

As before we initialize the app:

.. include:: owner_app_v1_code_00.rst

First, we create the User model. Of course, password would normally be encrypted, but note the use of a column class of `WriteOnlyColumn`. What this means is that when the returning results, the password would be automatically excluded, which can limit awkward mistakes, even when appropriately encrypted.

.. include:: owner_app_v1_code_01.rst

Next, we create an Order model. Think of this as some useful service that is requested by the user. An order has a life-cycle of *ordered*, *processed*, *complete*, and *cancelled*. For simplicity we will use codes from 0 to 3 respectively.

.. include:: owner_app_v1_code_02.rst

Now we create the database and create a couple users.

.. include:: owner_app_v1_code_03.rst

The point of this example is to show how to control restricted services and make modifications. Accordingly, we will gloss over the portion of the API for the user register/confirm/log-in process by simply creating users and focus on the creation of orders.

.. include:: owner_app_v1_code_04.rst

Create the Owner-Based Resources
--------------------------------

Since control is to be record-based, not table-based, we will need to know

* who is the user?
* permit the user to see only what records this user is permitted

To that end, we will create a subclass of ModelResource and CollectionModelResource that will take advantage of Flask-RESTful method decorators and combine it with a minor modification to a ModelResource and CollectionModelResource. That way we can code down on total code.

An OwnerResource and OwnerCollectionResource will created.

Mock Authentication
-------------------

We will create a mock authentication method decorator that is loosely based on Flask-JWT-Extended.

.. include:: owner_app_v1_code_05.rst

`mock_jwt_required()` provides the gatekeeping for access to the method. `get_identity()` extracts the authenticated user from the header. Together, they will provide the basis for inserting knowledge of the user in question to guide access to the right resources.

We are using this simple version, but a 'real' one, aside from actually being secure, might use admin and user roles and user status as other considerations.

Owner Resources
---------------

Once we create the subclass Owner resources to have the right combination of method decorators and processing of inputs, we will in turn subclass the owner resources.

.. include:: owner_app_v1_code_06.rst

Create the Order Resources
------------------------
Now we create the order resources. And, the code is minimal.

.. include:: owner_app_v1_code_07.rst


At this point we are ready to instantiate these resources with the API and fire up the app.

.. include:: owner_app_v1_code_08.rst


Use the API
-----------

First, we will attempt to post an order.

* Post without authentication
* Post an order wrong login
* Post an order that is correct
* Get the order collection with the right user

Post without authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v1_00.rst

Post An Order, Wrong Login
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v1_01.rst

Post An Order That Is Correct
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v1_02.rst

Get the Order Collection, No Authorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v1_03.rst

Get the Order Collection, Wrong User
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v1_04.rst

Get the Order Collection, Right User
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v1_05.rst

Order Meta Resource Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v1_06.rst

Order Meta Collection Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. include:: owner_app_v1_06.rst

