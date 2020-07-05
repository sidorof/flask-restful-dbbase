========================
Limited Method Resources
========================
Sometimes a pure REST approach does not fit the problem. For example, suppose a URL primarily represents an action. If the problem still interacts with the database in some fashion, it may be appropriate to create a resource that is limited in the methods that it exposes.

Create Resource
---------------

The `create_resource` function can create a resource with a custom configuration. The basic principals:

* Specify the name of the resource.
* Use a prototype resource class to model it on.
* Specify a model_class to use.
* Specify which methods to implement. If there is a `process_{method}_input` function in your prototype resource, it will be included.
* You can set `url_prefix` and `url_name` if necessary.
* You can overwrite any of the class variables to customize further your new resource by including a dict of class variables.
* Finally, the new resource will be created.


.. code-block:: python

    MyResource = create_resource(
        name="MyResource",
        resource_class=ModelResource,
        model_class=MyModel,
        methods=["post"],
        url_prefix="/",
        url_name="custom-action",
        class_vars={
            "process_post_input": custom_input_processing,
            "after_commit": {
                "post": special_function
            }
        }
    )

..

The above will create `MyResource` with only the POST method, which can then be added to the api just as any resource.

Caveat
------
When using a package, there can be tendency to try to do *everything* with it. Sometimes it is simply easier do it another way. As a general guideline for using these resources, some following conditions might be considered:

*   Does the method benefit from automatic enforcement of primary keys in the URL? If it is a problem not a benefit, the regular Flask-RESTful Resource class might be a better choice.
*   Is a connection to a database only minor portion of the work that is done? Maybe there is no benefit to a `model_class` central to a resource.
*   Do you struggle to define the problem within the context of Flask-RESTful-DBBase, but you know it could be done more simply outside of it? Do it that other way.

The beauty of Flask in part flows from being able to mix and match capabilities from all sorts of extensions, so it may be that Flask-RESTful-DBBase can handle the portions of the puzzle that fit without getting in the way of other approaches better suited to that portion of the system.

Further
-------
An example of this kind of usage is available in :ref:`Register App`
