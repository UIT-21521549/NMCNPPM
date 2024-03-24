import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from src.database.user import User

# TODO: use sqlalchemy.engine.URL
connection_string=os.getenv("db_connection_string")

db_engine = create_engine(connection_string)

user = User(db_engine)