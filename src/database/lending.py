from sqlalchemy import select, insert, null, update
from .connection import Session

from .models import (
    lending_table,
    lending_detail_table,
    fines_collection_table,
    book_table
)


def add_book_to_lending(lending_id, book_ids, quantities,session=None):
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
    assert len(book_ids) == len(quantities)

    stmt = insert(lending_table).values(
        user_id=user_id
    )

    lending_id = session.execute(stmt).inserted_primary_key[0]

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

    stmt = select(
        lending_table, lending_detail_table.c["book_id", "quantity"]
    ).join(lending_detail_table)

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
                "return_date": items[0]["return_date"],
                "penalty": items[0]["penalty"],
                "items": [
                    {"book_id": i["book_id"], "quantity": i["quantity"]} for i in items
                ],
            }
        )

    return result

# def return_lending(lending_id, session=None):
#     lending = get_lending([lending_id], session=session)
#     assert len(lending) == 1
#     lending = lending[0]

#     assert 