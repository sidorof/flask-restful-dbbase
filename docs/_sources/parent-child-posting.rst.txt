===========================
Parent Post - Child Records
===========================

Since some kinds of records by their nature are really a set consisting of a parent record and a list of child records. In this section we will look at an example for efficiently handling that.

Our example is that of an invoice. Suppose an invoice is created with 20 items. If we follow a purely REST approach, we would create a parent invoice followed by another 20 trips to the database for each item. Or, we could implement a collection POST resource for the invoice items and only have two trips. In that case, one trip for the parent and one for the set of invoice items.

With Flask-RESTful-DBBase, we will do it in one trip in the following example.

As before the code for this example is found in the examples section as

.. container:: default

    invoice_app <https://sidorof.github.io/flask-restful-dbbase/examples/invoice_app.py>
..


Create the database models
--------------------------

When we create our two tables to make up an invoice, note how the `invoice_items` relation is specified with `backref`. That means that the InvoiceItem will also have a field called `invoice`. And, it invokes a bidirectional update capability between an invoice and the set of invoice items.

.. include:: invoice_app_code_00.rst

Create the Invoice Resource
---------------------------

The InvoiceResource is pretty standard. There is one twist, unrelated to the topic at hand. Because we are using Sqlite3 as the default database, the invoice date that is sent as a string is not properly processed by Sqlite3. Converting a date string to a datatime object takes some time, so if your database automatically does this, there is no need for the extra step.

In this case, however, we will use `use_date_conversion` to signify that the API should do the conversion for us.

.. include:: invoice_app_code_01.rst

Finish the Rest of the Invoice Resources
----------------------------------------
The following resources are consistent with the other examples with nothing else that is special.


.. include:: invoice_app_code_02.rst

Add the Resources to the API
------------------------------

Finally, as before the resources are added to the API and we are ready for business.

.. include:: invoice_app_code_03.rst

Use the API
-----------

Create an Invoice
^^^^^^^^^^^^^^^^^

We will now create an invoice. The data consists of both the invoice portion and a list of line items that are to be added to the invoice. See how the `invoice_id` is left off of the invoice items data. While it is unknowable until the invoice is created, SQLAlchemy automatically fills it in when posting the line items.

.. include:: invoice_app_00.rst

Get an Invoice:
^^^^^^^^^^^^^^^
And we can GET an invoice with its related line items.

.. include:: invoice_app_01.rst

Meta Information for Invoice Post
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By examining the meta information for an invoice we can also determine whether we have the correct settings to create invoice items with the invoice.

If you look at `input` section and `invoiceItems`, it shows `readOnly` as False, meaning that it is updatable.

.. include:: invoice_app_02.rst


Caveat
-------

This ability to post child records with the parent is only implemented in the POST method. It is probably more efficient to update individual line items if using PUT or PATCH avoiding reconciliation issues related to alterations of existing records.


