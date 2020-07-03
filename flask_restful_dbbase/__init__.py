# flask_restful_dbbase/__init__.py
from flask_sqlalchemy import SQLAlchemy, BaseQuery

from dbbase import DB
from dbbase.model import Model
from dbbase.column_types import WriteOnlyColumn

from .resources import DBBaseResource, ModelResource, CollectionModelResource
from ._version import __version__


class DBBase(SQLAlchemy):
    def __init__(
        self,
        app=None,
        use_native_unicode=True,
        session_options=None,
        metadata=None,
        query_class=BaseQuery,
        model_class=Model,
        engine_options=None,
    ):
        super().__init__(
            app=app,
            use_native_unicode=use_native_unicode,
            session_options=session_options,
            metadata=metadata,
            query_class=BaseQuery,
            # Note that this is DBBase's Model
            model_class=Model,
            engine_options=engine_options,
        )

        self._include_dbbase()
        self.Model.db = self

    def _include_dbbase(self):
        """_install_dbbase functions

        This function adds the relevant dbbase functions

        So this is the only clutter added to the SQLAlchemy namespace
        There is more in Model.
        """
        setattr(DBBase, "WriteOnlyColumn", WriteOnlyColumn)
        setattr(DBBase, "doc_tables", DB.doc_tables)
        setattr(DBBase, "doc_table", DB.doc_table)
        setattr(DBBase, "doc_column", DB.doc_column)
        setattr(DBBase, "_process_table_args", DB._process_table_args)

        # add flask_sqlalchemy specific items to stop list
        Model._DEFAULT_SERIAL_STOPLIST.append("query_class")

        self.Model.db = self
