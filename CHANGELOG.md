# Changelog
## (0.1.7) -
### Added
*   Added a modification to the handling of ModelResource.serial_fields to enable a dictionary of a foreign class and serial fields to be returned when replacing the current Model class with another on responses.

### Changed
*   Corrected approach for default URLs for meta resources. Now the generation of the default URL stems from the root of the model resource.

For example, if the model resource URL is `/products`, then the meta resources URLs will be `/meta/products/single` or `/meta/products/collection`. However if the prefix for products is changed to `/api/v1/products`, then the meta resources URLs will be `/api/v1/meta/products/single` or `/api/v1/meta/products/collection`.


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
