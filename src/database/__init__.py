from .connection import Session, create_new, debug_mode
import src.database.user as USER
import src.database.book as BOOK
import src.database.parameters as PARAM
import src.database.lending as LENDING

import src.database.image as IMAGE
from .add_dummy_data import set_up
import os

if create_new:
    admin_password = os.getenv("admin_password")
    session = Session()
    # add parameters
    PARAM.init_parameter_table(session)
    session.commit()
    
    # create admin user
    USER.create_user(
        email="admin@admin", password=admin_password, user_name="admin", is_admin=True, session=session
    )

    if debug_mode:
        # create dummy data
        set_up(session)
    
    session.commit()
    session.close()