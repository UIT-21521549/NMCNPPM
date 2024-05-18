from sqlalchemy import select, insert, null, update
import jwt
import os
from datetime import datetime, timezone, timedelta, date
from hashlib import sha256

from .models import user_table, reader_type_table, fines_collection_table
from .connection import Session
from .parameters import get_parameter

from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def create_user(
    email,
    password,
    reader_type_id=null(),
    user_name=null(),
    birthday=null(),
    address=null(),
    is_admin=False,
    session=None,
):
    assert isinstance(email, str)
    assert isinstance(password, str)

    # TODO: check birthday and validate input

    param = get_parameter(session=session)
    minimum_age = param["minimum_age"]
    maximum_age = param["maximum_age"]

    if birthday is not null():
        birthday = datetime.strptime(birthday, "%d-%m-%Y").date()
        age = calculate_age(birthday)
        assert minimum_age <= age and maximum_age > age

    password_hash = sha256(str(password).encode("utf-8")).hexdigest()

    stmt = (
        insert(user_table)
        .values(
            reader_type_id=reader_type_id,
            email=email,
            password_hash=password_hash,
            user_name=user_name,
            birthday=birthday,
            address=address,
            is_admin=is_admin,
        )
        .returning(user_table.c["user_id", "created_at"])
    )

    result = session.execute(stmt).all()

    assert len(result) == 1

    user_id, created_at = result[0]

    # admin account does not have expiry date
    if is_admin:
        return user_id

    maximum_account_age = param["maximum_account_age"]

    # now update the expiry_date of user
    stmt = (
        update(user_table)
        .where(user_table.c.user_id == user_id)
        .values(expiry_date=created_at + timedelta(days=maximum_account_age))
    )

    session.execute(stmt)

    # return user_id
    return user_id


def get_users(user_ids=None, session=None):
    # return all if user_ids is None
    stmt = (
        select(
            user_table.c[
                "user_id",
                "reader_type_id",
                "email",
                "birthday",
                "address",
                "user_name",
                "created_at",
                "is_admin",
                "expiry_date",
                "penalty_owed"
            ],
            reader_type_table.c.reader_type,
            fines_collection_table.c[
                "fine_collection_id",
                "amount"
            ]
        )
        .join(reader_type_table, isouter=True)
        .join(fines_collection_table, isouter=True)
    )

    if user_ids is not None:
        stmt = stmt.where(user_table.c.user_id.in_(user_ids))

    rows = session.execute(stmt).all()

    assert len(rows) != 0

    rows = [i._asdict() for i in rows]

    u_id = list(set([i["user_id"] for i in rows]))

    result = []
    for idx in u_id:
        items = [i for i in rows if i["user_id"] == idx]

        result.append(
            {
                "user_id": idx,
                "reader_type_id": items[0]["reader_type_id"],
                "email": items[0]["email"],
                "birthday": items[0]["birthday"],
                "address": items[0]["reader_type_id"],
                "user_name": items[0]["user_name"],
                "created_at": items[0]["created_at"],
                "is_admin": items[0]["is_admin"],
                "expiry_date": items[0]["expiry_date"],
                "penalty_owed": items[0]["penalty_owed"],
                "fine_collections": [
                    {
                        "fine_collection_id": i["fine_collection_id"],
                        "amount": i["amount"],
                    }
                    for i in items if i["fine_collection_id"] is not None
                ],
            }
        )

    return result

def get_user_by_email(user_email, session=None):
    stmt = select(user_table.c.user_id).where(
        user_table.c.email==user_email
    )
    rows = session.execute(stmt).all()

    user_id = [i._asdict()["user_id"] for i in rows]

    assert len(user_id) == 1

    user_id = user_id[0]

    return get_users([user_id], session=session)


def create_reader_type(reader_type, session=None):
    assert isinstance(reader_type, str)

    stmt = insert(reader_type_table).values(reader_type=reader_type)

    result = session.execute(stmt)

    # return reader_type_id
    return result.inserted_primary_key[0]


def get_reader_type(reader_type_id=None, session=None):
    # return all if reader_type_id is None

    stmt = select(reader_type_table)

    if reader_type_id is not None:
        stmt = stmt.where(reader_type_table.c.reader_type_id == reader_type_id)

    result = session.execute(stmt).all()

    assert len(result) != 0

    return [i._asdict() for i in result]


# login with email and password
def verify_user(email, password, session=None):
    assert isinstance(email, str)
    assert isinstance(password, str)

    password_hash = sha256(str(password).encode("utf-8")).hexdigest()

    stmt = (
        select(user_table)
        .where(user_table.c.email == email)
        .where(user_table.c.password_hash == password_hash)
    )

    result = session.execute(stmt).first()._asdict()

    return result


def create_jwt_token(email, password, session=None):
    jwt_secret = os.getenv("jwt_secret")
    assert jwt_secret is not None

    user = verify_user(email, password, session=session)

    assert user is not None

    payload = {
        "user_id": user["user_id"],
        "is_admin": user["is_admin"],
        # hết hạng sau 2 ngày
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=2),
    }

    token = jwt.encode(payload, jwt_secret, algorithm="HS256")

    return {"token": token, "user_id": user["user_id"]}


def verify_jwt_token(token):
    jwt_secret = os.getenv("jwt_secret")
    assert jwt_secret is not None

    # will raise error if token is invalid
    payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])

    return {
        "user_id": payload["user_id"],
        "is_admin": payload["is_admin"],
    }


def pay_penalty(user_id, amount, session=None):

    update_stmt = (
        update(user_table)
        .where(user_table.c.user_id == user_id)
        .values(penalty_owed=user_table.c.penalty_owed - amount)
    )

    session.execute(update_stmt)

    stmt = insert(fines_collection_table).values(user_id=user_id, amount=amount)
    result = session.execute(stmt)

    return result.inserted_primary_key[0]


def get_penalties_paid(user_id=None, session=None):
    stmt = select(fines_collection_table)

    if user_id is not None:
        stmt = stmt.where(fines_collection_table.c.user_id == user_id)

    result = session.execute(stmt).all()

    assert len(result) != 0

    return [i._asdict() for i in result]
