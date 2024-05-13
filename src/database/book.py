from sqlalchemy import select, insert, null, desc, asc

from .models import (
    book_title_table,
    book_genre_table,
    author_table,
    book_author_list,
    publisher_table,
    book_table,
    book_receipt_table,
    book_receipt_detail_table,
)


def create_genre(genre_name, session=None):
    stmt = insert(book_genre_table).values(
        genre_name=genre_name,
    )
    result = session.execute(stmt)

    # return genre_id
    return result.inserted_primary_key[0]


def get_genre(genre_id=None, session=None):
    # return all if genre_id is None

    stmt = select(book_genre_table)

    if genre_id is not None:
        stmt = stmt.where(book_genre_table.c.genre_id == genre_id)

    result = session.execute(stmt).all()

    assert len(result) != 0

    return [i._asdict() for i in result]


def create_author(author_name, session=None):
    stmt = insert(author_table).values(
        author_name=author_name,
    )

    result = session.execute(stmt)

    # return author_id
    return result.inserted_primary_key[0]


def get_author(author_id=None, session=None):
    # return all if author_id is None
    stmt = select(author_table)

    if author_id is not None:
        stmt = stmt.where(author_table.c.author_id == author_id)

    result = session.execute(stmt).all()

    assert len(result) != 0

    return [i._asdict() for i in result]


def create_publisher(publisher_name, session=None):
    stmt = insert(publisher_table).values(
        publisher_name=publisher_name,
    )

    result = session.execute(stmt)

    # return publisher_id
    return result.inserted_primary_key[0]


def get_publisher(publisher_id=None, session=None):
    # return all if publisher_id is None

    stmt = select(publisher_table)

    if publisher_id is not None:
        stmt = stmt.where(publisher_table.c.publisher_id == publisher_id)

    result = session.execute(stmt).all()

    assert len(result) != 0

    # [(publisher_id, publisher_name)]
    return [i._asdict() for i in result]


def create_book_title(book_name, genre_id, session=None):

    stmt = insert(book_title_table).values(book_name=book_name, genre_id=genre_id)

    result = session.execute(stmt)

    # return book_title_id
    return result.inserted_primary_key[0]


def get_book_title(book_title_ids=None, session=None):
    # book_title_ids is list of id
    # return all if book_title_ids is None

    stmt = (
        select(book_title_table, book_genre_table.c.genre_name, author_table)
        .join(book_genre_table)
        .join(book_author_list)
        .join(author_table)
    )
    if book_title_ids is not None:
        stmt = stmt.where(book_title_table.c.book_title_id.in_(book_title_ids))

    rows = session.execute(stmt).all()

    assert len(rows) != 0

    rows = [i._asdict() for i in rows]

    bt_id = list(set([i["book_title_id"] for i in rows]))

    result = []
    for idx in bt_id:
        items = [i for i in rows if i["book_title_id"] == idx]

        result.append(
            {
                "book_title_id": idx,
                "genre_id": items[0]["genre_id"],
                "book_name": items[0]["book_name"],
                "genre_name": items[0]["genre_name"],
                "image_id": items[0]["image_id"],
                "authors": [
                    {"author_id": i["author_id"], "author_name": i["author_name"]}
                    for i in items
                ],
            }
        )
    return result


def add_authors_to_book(book_title_id, author_ids, session=None):

    result = session.execute(
        insert(book_author_list),
        [{"book_title_id": book_title_id, "author_id": i} for i in author_ids],
    )

    return True


def create_book(book_title_id, publication_year, publisher_id, price, session=None):

    stmt = insert(book_table).values(
        book_title_id=book_title_id,
        publication_year=publication_year,
        publisher_id=publisher_id,
        price=price,
    )

    result = session.execute(stmt)

    # return book_id
    return result.inserted_primary_key[0]


def get_book(book_ids=None, session=None):
    # return all if book_title_id is None

    stmt = (
        select(
            book_table,
            publisher_table.c.publisher_name,
        )
        .select_from(book_table)
        .join(publisher_table)
    )

    if book_ids is not None:
        stmt = stmt.filter(book_table.c.book_id.in_(book_ids))

    result = session.execute(stmt).all()

    assert len(result) != 0

    return [i._asdict() for i in result]


def get_n_newly_added_book_title(n=4, session=None):
    # order by book_receipt entry_date

    stmt = (
        select(book_receipt_table, book_table.c.book_title_id)
        .select_from(book_receipt_table)
        .join(book_receipt_detail_table)
        .join(book_table)
        .order_by(desc(book_receipt_table.c.entry_date))
        .group_by(book_table.c.book_title_id, book_receipt_table.c.entry_date)
        .limit(n)
    )

    results = session.execute(stmt).all()

    book_title_ids = [i._asdict()["book_title_id"] for i in results]


    return get_book_title(book_title_ids, session=session)


def get_book_title_details(book_title_id, session=None):
    book_title = get_book_title(book_title_id=book_title_id, session=session)

    assert len(book_title) == 1

    book_title = book_title[0]

    stmt = (
        select(book_table, publisher_table.c.publisher_name)
        .select_from(book_table)
        .where(book_table.c.book_title_id == book_title["book_title_id"])
    )
    result = session.execute(stmt).all()

    book_title["editions"] = [i._asdict() for i in result]

    return book_title


def add_book_to_receipt(book_receipt_id, book_ids, quantities, session=None):

    result = session.execute(
        insert(book_receipt_detail_table),
        [
            {"book_receipt_id": book_receipt_id, "book_id": i, "quantity": q}
            for i, q in zip(book_ids, quantities)
        ],
    )


def create_book_receipt(book_ids=[], quantities=[], session=None):
    assert len(book_ids) == len(quantities)

    stmt = insert(book_receipt_table)

    book_receipt_id = session.execute(stmt).inserted_primary_key[0]

    assert book_receipt_id is not None

    if len(book_ids) > 0:
        add_book_to_receipt(
            book_receipt_id=book_receipt_id,
            book_ids=book_ids,
            quantities=quantities,
            session=session,
        )

    return book_receipt_id


def get_book_receipt(book_receipt_id=None, session=None):
    # return all if book_receipt_id is None

    stmt = select(
        book_receipt_table, book_receipt_detail_table.c["book_id", "quantity"]
    ).join(book_receipt_detail_table)

    if book_receipt_id is not None:
        stmt = stmt.where(book_receipt_table.c.book_receipt_id == book_receipt_id)

    rows = session.execute(stmt).all()

    assert len(rows) != 0

    rows = [i._asdict() for i in rows]

    bt_id = list(set([i["book_receipt_id"] for i in rows]))

    result = []
    for idx in bt_id:
        items = [i for i in rows if i["book_receipt_id"] == idx]

        result.append(
            {
                "book_receipt_id": idx,
                "entry_date": items[0]["entry_date"],
                "items": [
                    {"book_id": i["book_id"], "quantity": i["quantity"]} for i in items
                ],
            }
        )
    return result
