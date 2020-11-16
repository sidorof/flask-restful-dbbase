# Changelog
## (0.3.4) -
### Changed
*   Added tests for null values in functions in dbbase_resource that verify value types.

## (0.3.3) -
### Changed
*   Changed screen_data function in DBBaseResource to remove additional extraneous data.

## (0.3.2) -
### Changed
*   Removed super from CollectionModelResource.
*   Added `query_string` for multiple values. Axios, for example, uses a notation such as `('statusId[]', '0'), ('statusId[]`. To accommodate that the query string looks for variables ending with `[]` and converts a query to search for values in a list.

An example of the following styles for query strings with arrays are now supported:

```
    statusId[]=1&statusId[]=2&owner_id=1
    statusId=[1,2]&owner_id=1
    statusId=1&statusId=2&owner_id=1
    statusId=1,2&owner_id=1&debug=false

```

## (0.3.1) -
### Changed
* Reinstated the `requirements` key in method docs, which had erroneously dropped off in the rewrite.

## (0.3.0) -
### Changed
* Rewrote approach to documentation functions. Expanded the MetaDoc class, added a MethodDoc class. This enables a standardized scaffolding for all the documentation functions, and all meta documentation creation is performed by these classes.

## (0.2.5) -
### Add
*   Added an ability to document the internal processes that can shape the inputs and data records. To simplify the process a utility class, `MetaDoc`, has been added to `utils.py` to provide a scaffolding to hold the documentation. Adding a meta doc class to a model resource enables documentation for the `process_{method}_input` functions as well as the before/after commit functions. Finally, since control via these functions can affect the resource responses, there is an `exclude` flag in the MetaDoc class. Adding a method to exclude will mean that meta information would rely on your description regarding whichever function causes the resource to end in non-traditional manner.

### Changed
*   The example `post_only_resource` has been modified to include custom documentation from an after_commit function as well as out for meta information for this resource.

## (0.2.4) -
### Changed
*   More work on query inputs in meta info. Removed extraneous properties from queries. Now it includes only type, format, maxLength, properties needed to understand the kind of data for filtering queries.

## (0.2.3) -
### Changed
*   Changed key `query_string` to `queryString` in meta info to be more consistent with JavaScript standards for its intended use.

## (0.2.2) -

### Changed
+   Changed meta information `url_part` to simply `url`.
*   Changed flag for creating a url for meta information for a collection. It previously uses issubclass to identify a collection model resource. However, that fails when using the `generator.create_resource` function due to a reduced mro stack. It now keys off the `is_collection` function.
*   Changed meta information keys to better conform to JavaScript standards, since it is more likely to be used in that environment. `url_prefix` -> `urlPrefix`, etc.

## (0.2.1) -

### Added
* Add filtering for meta information. Meta information is very thorough. If the point of the meta information is to be able
to look up a section to see what happens in that spot, then being to filter the meta info cuts down significantly on the volume.

    `/meta/products/single?method=get&filter=table`

The above returns the contents of the get method along with
details of the underlying table.

    `/meta/products/single?method=get&filter=table`

The request below returns just the inputs available for post.

    `/meta/products/single?method=post&filter=input`


## (0.2.0) -
This version breaks previous before / after commmit functions in ModelResource. By requiring a status flag as output from the functions it opens resources to be more easily used beyond simply REST functions.

### Added
* Added a create_resource function that can create resources constrained to a limited HTTP method. Coupled with the refactored functions that can run after posting, a resource can be used for RPC-like features for when the REST is not a good fit.

### Changed
* Removed a redundant line in `DBBase._include_dbbase`.
* Refactored before/after commit functions in ModelResource. Just as the `process_{method}_input` functions return a status with the payload, these functions now return a status as well as a payload. Prior to this change, the assumption of the process was that there may be changes to a database item, or a database item would be replaced with another, but once an adjustment takes place it all goes to an inevitable conclusion of returning SOME item and a status codde. By adding this, a greater range of functionality with the ModelResource is available, including returning simply a message and a status code. In such a case, a ModelResource could use the serialization / validation services, but essentially act as an RPC if need be.

## (0.1.11) -
### Changed
* Corrected and simplified the selection of primary keys in `DBBaseResource.get_key_names`.

## (0.1.10) -
### Changed
* Ensured that response fields for meta information were in camel case format. Table property fields remain in snake case to be consistent for usage within Python.

## (0.1.9) -
### Changed
* Modified setup and requirements.txt files for additional required packages.

## (0.1.8) -
### Changed
# Changelog
* Corrected issue with the response meta docs which did not correctly pull modified serial lists from Model configuration.

## (0.1.7) -
### Added
*   Added a modification to the handling of ModelResource.serial_fields to enable a dictionary of a foreign class and serial fields to be returned when replacing the current Model class with another on responses.
*   Added Parent/Child processing in POST. This enables the creation of child records as part of the commit process of a parent.
*   Added an example program creating an invoice with invoice line items at the same time.

### Changed
*   Corrected approach for default URLs for meta resources. Now the generation of the default URL stems from the root of the model resource.

For example, if the model resource URL is:


    /products


then the meta resources URLs will be


    /meta/products/single
    /meta/products/collection


However if the prefix for products is changed to


    /api/v1/products


then the meta resources URLs will be


    /api/v1/meta/products/single or
    /api/v1/meta/products/collection


## (0.1.6) -
### Added
*   Added more tests on resources - coverage is now 98%
*   Added more sections to documentation of resources

### Changed
*   Changed default URLs. Added pluralizer for default URLs. Now a model `Book` will default to a URL of `/books`
*   Tightened up processing on process_{method}_input functions to a more standardized with more complete documentation.

## (0.1.5) -
### Changed
* Corrected the project location with hyphens instead of underlines
* Corrected typo in the setup description


## (0.1.1) -
### Added
* Added ModelResource for datacentric methods that are not collections.
* Added tests using unittest and pytest.

## (0.1.0) -
### Added
- Initial public release
