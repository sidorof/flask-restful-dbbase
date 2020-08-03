---------------------------
Limited Method Resources
---------------------------
Sometimes a pure REST approach does not fit the problem. For example, suppose a URL primarily represents an action. If the problem still interacts with the database in some fashion, it may be appropriate to create a resource that is limited in the methods that it exposes.

Create Resource
---------------

The `create_resource` function can create a resource with a custom configuration. The basic principals:

* Specify the name of the resource.
* Use a prototype resource class to model it on.
* Specify a model_class to use.
* Specify which methods to implement. If there is a `process_{method}_input` function in your prototype resource, it will be included.
* You can set `url_prefix` and `url_name` if necessary.
* You can overwrite any of the class variables to customize your new resource further by including a dict of class variables.
* Finally, the new resource will be created.

.. code-block:: python

    PostOnlyResource = create_resource(
        name="PostOnlyResource",
        resource_class=ModelResource,
        model_class=Whatever,
        methods=['post'],
        url_prefix=None,
        url_name=None,
        class_vars={
            "after_commmit": {
                "post": my_procedure
            }
        },
    )

..

Suggested Uses
--------------
* **/register:** POST using a User class model. A confirmation email is sent. A message is returned with instructions in place of the posted user data.
* A command is run that uses deserialization / validation services but goes on to execute the command.

.. note::

    One thing to consider regarding these alterations is the degree of change wanted from a REST format. For example, a POST method with REST excludes posting an existing data item. Flask-RESTful-DBBase automatically verifies that there is no existing record as a benefit.

    If that is not suitable for the application, another alternative would be to create a resource from the proto resource, DBBaseResource. With it are functions for screening data, etc., and you could create your own POST method.



Example
-------

As before, the code for this example is found in the examples section as

.. container:: default

    post_only_resource <https://github.com/sidorof/flask-restful-dbbase/blob/master/examples/post_only_resource.py>
..

To give a concrete example, we will create a resource limited to a POST method. The following shows an example of the usual initialization with the exception of the `generator.create_resource` program. This program accepts a source resource. From it `create_resource` will generate a resource in a custom configuration.

There are two additional features imported, `create_resource` and `MetaDoc`.

.. include:: post_only__code_00.rst

The table created is minimal for this example.

.. include:: post_only__code_01.rst

We will divert processing of a POST to exit just after a commit to the database. To that end, the following is a minimal `after_commit` function that will execute.

The sign that a normal return of the posted data does not happen can be seen at the return. The return tuple starts with a False.

.. include:: post_only__code_02.rst

Having defined our exit function, we can now create the resource itself. The following shows that creation. The parameters give some flexibility of output.

* The source resource class is ModelResource in this case, although it could be a subclassed resource.
* Only the POST method is implemented.
* Like any ModelResource, the url_prefix and url_name can be set explcitly.
* Finally, the `class_vars` provides a means to set any attribute of the new class. In this case we will use that feature to set the `after_commit` function created above.

.. include:: post_only__code_03.rst

Because we have caused the resource to give output outside of a standard REST response, meta information associated with this method does not fit the new reality. To accommodate this, we will use a new feature, the `meta_doc` attribute. This is an instance of the `MetaDoc` found in `utils.py`. It presents a structure to place documentation for functions, and also a flag to exclude the standard responses when it is not relevant.

.. include:: post_only__code_04.rst


The following shows the addition of the resources and startup of the app.

.. include:: post_only__code_05.rst


Using the API
-------------

We POST data to the URL. Data deserialization and validation takes place as usual. And, because this is an after_commit function, it is saved to the database. The result shows the non-REST response to the entry.

.. include:: post_only_00.rst

Generating the meta information can reflect that the usual output has been replaced with our new message.

.. include:: post_only_01.rst
