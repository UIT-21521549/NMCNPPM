from sqlalchemy import select, insert, null, update
from .connection import Session, debug_mode
from datetime import datetime, timezone, timedelta, date
from sqlalchemy.sql import func
from .parameters import get_parameter
from .user import get_users

from .models import (
    lending_table,
    lending_detail_table,
    fines_collection_table,
    book_table,
    user_table,
)
import random


def add_book_to_lending(lending_id, book_ids, quantities, session=None):
    assert len(book_ids) == len(quantities)

    session.execute(
        insert(lending_detail_table),
        [
            {"lending_id": lending_id, "book_id": i, "quantity": q}
            for i, q in zip(book_ids, quantities)
        ],
    )
    # update the available book counter
    # this will fail if there is not enough book to lend
    for i, q in zip(book_ids, quantities):
        session.execute(
            update(book_table)
            .where(book_table.c.book_id == i)
            .values(available=book_table.c.available - q)
        )


def create_book_lending(user_id, book_ids=[], quantities=[], session=None):

    user_expiry_date = get_users([user_id], session=session)[0]["expiry_date"]

    diff = datetime.now() - user_expiry_date

    assert diff.days < 0

    assert len(book_ids) == len(quantities)

    stmt = (
        insert(lending_table)
        .values(user_id=user_id)
        .returning(lending_table.c["lending_id", "lending_date"])
    )

    result = session.execute(stmt).all()
    assert len(result) == 1

    lending_id, lending_date = result[0]

    # update return deadline

    maximum_lending_period = get_parameter("maximum_lending_period", session=session)

    stmt = (
        update(lending_table)
        .where(lending_table.c.lending_id == lending_id)
        .values(return_deadline=lending_date + timedelta(days=maximum_lending_period))
    )

    session.execute(stmt)

    if len(book_ids) > 0:
        add_book_to_lending(
            lending_id=lending_id,
            book_ids=book_ids,
            quantities=quantities,
            session=session,
        )

    return lending_id


def get_lending(lending_ids=None, session=None):
    # return all if lending_ids is None

    stmt = select(lending_table, lending_detail_table.c["book_id", "quantity"]).join(
        lending_detail_table
    )

    if lending_ids is not None:
        stmt = stmt.where(lending_table.c.lending_id.in_(lending_ids))

    rows = session.execute(stmt).all()

    assert len(rows) != 0

    rows = [i._asdict() for i in rows]

    bt_id = list(set([i["lending_id"] for i in rows]))

    result = []
    for idx in bt_id:
        items = [i for i in rows if i["lending_id"] == idx]

        result.append(
            {
                "lending_id": idx,
                "user_id": items[0]["user_id"],
                "lending_date": items[0]["lending_date"],
                "return_deadline": items[0]["return_deadline"],
                "return_date": items[0]["return_date"],
                "penalty": items[0]["penalty"],
                "items": [
                    {"book_id": i["book_id"], "quantity": i["quantity"]} for i in items
                ],
            }
        )

    return result


def return_lending(lending_id, session=None):

    lending = get_lending([lending_id], session=session)[0]

    # lock the lending
    # this will fail if returned_lock have been locked
    stmt = (
        update(lending_table)
        .where(lending_table.c.lending_id == lending_id)
        .values(returned_lock=lending_table.c.returned_lock + 1, return_date=func.now())
        .returning(lending_table.c["return_deadline", "return_date", "user_id"])
    )

    return_deadline, return_date, user_id = session.execute(stmt).all()[0]

    # now update the available book counter

    for item in lending["items"]:
        book_id = item["book_id"]
        quantity = item["quantity"]

        session.execute(
            update(book_table)
            .where(book_table.c.book_id == book_id)
            .values(available=book_table.c.available + quantity)
        )

    # calculate the penalty
    days_late = (return_date - return_deadline).days

    if debug_mode:
        days_late = random.randrange(0, 10)

    if days_late > 0:
        penalty = days_late * 1000 * sum([i["quantity"] for i in lending["items"]])
        # update the penalty

        stmt = (
            update(lending_table)
            .where(lending_table.c.lending_id == lending_id)
            .values(penalty=penalty)
        )
        session.execute(stmt)

        # now add the new penalty to user's owed penalty
        stmt = (
            update(user_table)
            .where(user_table.c.user_id == user_id)
            .values(penalty_owed=user_table.c.penalty_owed + penalty)
        )
        session.execute(stmt)

def get_lending_by_user_id(user_id, session=None):

    stmt = select(lending_table.c.lending_id).where(
        lending_table.c.user_id == user_id
    )
    result = session.execute(stmt).all()

    lending_ids = [i[0] for i in result]

    if len(lending_ids) == 0:
        return []
    
    return get_lending(lending_ids=lending_ids, session=session)
