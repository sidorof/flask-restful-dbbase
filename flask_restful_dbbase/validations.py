# validations.py
import logging

logger = logging.getLogger(__name__)


def validate_process(output, true_keys, false_keys=None):
    false_keys = ["message", "status_code"]

    if not isinstance(output, dict):
        msg = f"Output must a dict: {type(output)}"
        logger.error(msg)
        raise ValueError(msg)

    if "status" in output:
        if not isinstance(output["status"], bool):
            msg = "'status' must be either True or False."
            logger.error(msg)
            raise ValueError(msg)

        if output["status"]:
            for key in true_keys:
                if key not in output:
                    msg = f"There must a '{key}' key in output"
                    logger.error(msg)
                    raise ValueError(msg)
        else:
            for key in false_keys:
                if key not in output:
                    msg = f"There must a '{key}' key in output"
                    logger.error(msg)
                    raise ValueError(msg)

    else:
        msg = "There must a 'status' key in output"
        logger.error(msg)
        raise ValueError(msg)
