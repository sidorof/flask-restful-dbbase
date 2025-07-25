# validations.py
"""
Module for validating outputs.
"""
from flask import current_app


def validate_process(output, true_keys, false_keys=None):
    false_keys = ["message", "status_code"]

    if not isinstance(output, dict):
        msg = f"Output must a dict: {type(output)}"
        current_app.logger.error(msg)
        raise ValueError(msg)

    if "status" in output:
        if not isinstance(output["status"], bool):
            msg = "'status' must be either True or False."
            current_app.logger.error(msg)
            raise ValueError(msg)

        if output["status"]:
            for key in true_keys:
                if key not in output:
                    msg = f"There must a '{key}' key in output"
                    current_app.logger.error(msg)
                    raise ValueError(msg)
        else:
            for key in false_keys:
                if key not in output:
                    msg = f"There must a '{key}' key in output"
                    current_app.logger.error(msg)
                    raise ValueError(msg)

    else:
        msg = "There must a 'status' key in output"
        current_app.logger.error(msg)
        raise ValueError(msg)
