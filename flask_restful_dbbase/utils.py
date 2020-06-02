# utils.py
"""
This module implements some utilities.
"""
#from .exceptions import ExistingRecord


def check_existing_id(id_name, data, model_class):
    """check_existing_id

    This function checks incoming data dict for an id to screen
    /item for existing records in POSTs.

    If there is an existing record, it returns an error message and
    response.status_code of 400.

    Args:
        data (dict) : incoming data
        model_class (cls) : the class used for the id check

    Returns:
        msg, status_code | Nonel
    """
    data_id = data.get(id_name)
    if data_id is not None:
        id = data[id_name]
        if model_class.query.get(id):
            name = model_class._class()

            msg = f"{name} already has an id of {id}"
            return True, msg, 409

    return False, None, None


def check_mismatch_ids(id, data):
    """
    When using PUT, it is possible to use /item/{id} or /item, but if
    the data has an id as well as the presence of a parameter id,
    then a check is performed to ensure there are no slip ups.

    Since this is for PUT, there must be an id in one or the other.

    Args:
        id (int) : the id that is the passed in parameter.
        data (dict) : a dict that potentially holds an id as well.
    """
    data_id = data.get('id')
    if data_id is not None:
        if id != int(data_id):
            msg = f'The url id, {id}, does not match the data id {data_id}.'
            return True, {"message": msg}, 409

    return False, None, None


