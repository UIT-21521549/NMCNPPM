import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import sqlalchemy
from src.database.models import metadata_obj

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import event
from sqlite3 import Connection as SQLite3Connection

from .db_constraints import metadata_obj

# https://stackoverflow.com/questions/2614984/sqlite-sqlalchemy-how-to-enforce-foreign-keys/15542046#15542046
def _fk_pragma_on_connect(dbapi_con, con_record):
    if isinstance(dbapi_con, SQLite3Connection):
        dbapi_con.execute("pragma foreign_keys=ON")

connection_string = os.getenv("db_connection_string")

debug_mode = False
if os.getenv("debug_mode"):
    debug_mode = True

db_engine = create_engine(connection_string, echo=False)

event.listen(db_engine, "connect", _fk_pragma_on_connect)

create_new = not sqlalchemy.inspect(db_engine).has_table("user")

if create_new:
    metadata_obj.create_all(db_engine, checkfirst=False)

session_factory = sessionmaker(db_engine)
Session = scoped_session(session_factory)
