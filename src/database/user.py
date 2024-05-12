from sqlalchemy import select, insert, null
import jwt
import os
from datetime import datetime, timezone, timedelta
from hashlib import sha256

from .models import user_table, reader_type_table
from .connection import Session


def create_user(
    email,
    password,
    reader_type_id=null(),
    user_name=null(),
    birthday=null(),
    address=null(),
    is_admin=False,
    Session=Session,
):
    assert isinstance(email, str)
    assert isinstance(password, str)

    # TODO: check birthday and validate input

    password_hash = sha256(str(password).encode("utf-8")).hexdigest()

    stmt = insert(user_table).values(
        reader_type_id=reader_type_id,
        email=email,
        password_hash=password_hash,
        user_name=user_name,
        birthday=birthday,
        address=address,
        is_admin=is_admin,
    )
    try:
        with Session() as session:
            result = session.execute(stmt)
            session.commit()
    except:
        # Todo: return error message
        return None

    # return user_id
    return result.inserted_primary_key[0]


def get_users(user_ids=None, Session=Session):
    # return all if user_ids is None
    stmt = select(
        user_table.c[
            "user_id",
            "reader_type_id",
            "email",
            "birthday",
            "address",
            "user_name",
            "is_admin",
        ],
        reader_type_table.c.reader_type,
    ).join(reader_type_table, isouter=True)

    if user_ids is not None:
        stmt = stmt.where(user_table.c.user_id.in_(user_ids))

    try:
        with Session() as session:
            result = session.execute(stmt)
    except:
        # Todo: return error message
        return None

    if result is None:
        return None

    return [i._asdict() for i in result]


def create_reader_type(reader_type, Session=Session):
    assert isinstance(reader_type, str)

    stmt = insert(reader_type_table).values(reader_type=reader_type)

    try:
        with Session() as session:
            result = session.execute(stmt)
            session.commit()
    except:
        # Todo: return error message
        return None

    if result is None:
        return None

    # return reader_type_id
    return result.inserted_primary_key[0]


def get_reader_type(reader_type_id=None, Session=Session):
    # return all if reader_type_id is None

    stmt = select(reader_type_table)

    if reader_type_id is not None:
        stmt = stmt.where(reader_type_table.c.reader_type_id == reader_type_id)

    try:
        with Session() as session:
            result = session.execute(stmt).all()
    except:
        # Todo: return error message
        return None
    
    if result is None:
        return None

    return [i._asdict() for i in result]


# login with email and password
def verify_user(email, password, Session=Session):
    assert isinstance(email, str)
    assert isinstance(password, str)

    password_hash = sha256(str(password).encode("utf-8")).hexdigest()

    stmt = (
        select(user_table)
        .where(user_table.c.email == email)
        .where(user_table.c.password_hash == password_hash)
    )

    try:
        with Session() as session:
            result = session.execute(stmt).first()._asdict()

    except:
        # Todo: return error message
        return None

    return result


def create_jwt_token(email, password, Session=Session):
    jwt_secret = os.getenv("jwt_secret")
    assert jwt_secret is not None

    user = verify_user(email, password, Session=Session)

    if user is None:
        return None

    payload = {
        "user_id": user["user_id"],
        "is_admin": user["is_admin"],
        # hết hạng sau 2 ngày
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=2),
    }

    token = jwt.encode(payload, jwt_secret, algorithm="HS256")

    return token


def verify_jwt_token(token):
    jwt_secret = os.getenv("jwt_secret")
    assert jwt_secret is not None

    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    except:
        return None

    return {
        "user_id": payload["user_id"],
        "is_admin": payload["is_admin"],
    }
