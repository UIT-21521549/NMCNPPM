from .connection import Session, create_new
import src.database.user as USER
import src.database.book as BOOK
from .set_up_db import set_up

if create_new:
    set_up()