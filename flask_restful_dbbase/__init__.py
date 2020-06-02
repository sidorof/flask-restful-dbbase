# flask_restful_dbbase/__init__.py
import os
from sqlalchemy import Table

from flask_sqlalchemy import SQLAlchemy, BaseQuery

from dbbase import DB
from dbbase.base import _filter_column_props
from dbbase.model import Model
from dbbase.column_types import WriteOnlyColumn

from . resources import DBBaseResource, ModelResource, CollectionModelResource
from ._version import __version__
from . queries import parse_query


class DBBase(SQLAlchemy):
    def __init__(self, app=None, use_native_unicode=True, session_options=None,
                 metadata=None, query_class=BaseQuery, model_class=Model,
                 engine_options=None):
        super().__init__(
            app=app,
            use_native_unicode=use_native_unicode,
            session_options=session_options,
            metadata=metadata,
            query_class=BaseQuery,
            model_class=Model,                  # Note that this is DBBase's Model
            engine_options=engine_options)

        self._include_dbbase()
        self.Model.db = self


    def _include_dbbase(self):
        """_install_dbbase functions

        This function adds the relevant dbbase functions

        So this is the only clutter added to the SQLAlchemy namespace
        There is more in Model.
        """
        setattr(DBBase, 'WriteOnlyColumn', WriteOnlyColumn)
        setattr(DBBase, 'doc_tables', DB.doc_tables)
        setattr(DBBase, 'doc_table', DB.doc_table)
        setattr(DBBase, 'doc_column', DB.doc_column)
        DBBase._filter_column_props = _filter_column_props
        setattr(DBBase, '_process_table_args', DB._process_table_args)

        # add flask_sqlalchemy specific items to stop list
        Model._DEFAULT_SERIAL_STOPLIST.append('query_class')

        self.Model.db = self


# def _apply_db(db):
#     """ _apply_db
#
#     This function walks the Model classes and inserts the query
#     and db objects. Applying db helps in situations where the
#     db has changed from the original creation of the Model.
#     """
#     for cls in db.Model._decl_class_registry.values():
#         if hasattr(cls, "__table__"):
#             if isinstance(cls.__table__, Table):
#                 cls.db = db
#

