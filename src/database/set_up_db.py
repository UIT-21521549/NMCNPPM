import os
from .connection import Session, create_new
import src.database.user as USER

def set_up():
    # create admin user
    admin_password = os.getenv("admin_password")

    USER.create_user(
        email="admin@admin",
        password=admin_password,
        user_name="admin",
        is_admin=True
    )

    for rt in ["X", "Y"]:
        USER.create_reader_type(reader_type=rt)
    
    # TODO add dummy data


