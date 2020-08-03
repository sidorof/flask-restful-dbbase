# flask_restful_dbbase/utils.py
"""
This module implements utilities.
"""


class MetaDoc(object):
    """
    This class provides a scaffolding for holding documentation
    used when generating meta documents.
    """

    methods = ("get", "post", "put", "patch", "delete")

    def __init__(self, **kwargs):

        # process input functions
        for method in self.methods:
            func_name = f"process_{method}_input"
            setattr(self, func_name, kwargs.get(func_name, None))

        # before / after functions
        self._before_commit = {}
        self._after_commit = {}
        for commit_func in ["before_commit", "after_commit"]:
            if commit_func in kwargs:
                for key, value in kwargs[commit_func].items():
                    func = getattr(self, commit_func)
                    func(key, value)

        # exclude responses
        self.excludes = set()
        excludes = kwargs.get("excludes", None)
        if excludes:
            for method in self.methods:
                if method in excludes:
                    self.excludes.add(method)

    def before_commit(self, method, text):
        if method in self.methods[1:]:
            self._before_commit[method] = text
        else:
            raise ValueError("This method is not valid")

    def after_commit(self, method, text):
        if method in self.methods[1:]:
            self._after_commit[method] = text
        else:
            raise ValueError("This method is not valid")
