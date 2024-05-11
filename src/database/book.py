from sqlalchemy import select, insert, null
from .connection import Session

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


def create_genre(genre_name, Session=Session):
    stmt = insert(book_genre_table).values(
        genre_name=genre_name,
    )
    try:
        with Session() as session:
            result = session.execute(stmt)
            session.commit()
    except:
        # Todo: return error message
        return None

    # return genre_id
    return result.inserted_primary_key[0]


def get_genre(genre_id=None, Session=Session):
    # return all if genre_id is None

    stmt = select(book_genre_table)

    if genre_id is not None:
        stmt = stmt.where(book_genre_table.c.genre_id == genre_id)

    try:
        with Session() as session:
            result = session.execute(stmt).all()
    except:
        # Todo: return error message
        return None

    # [(genre_id, genre_name)]
    return [i._asdict() for i in result]


def create_author(author_name, Session=Session):
    stmt = insert(author_table).values(
        author_name=author_name,
    )

    try:
        with Session() as session:
            result = session.execute(stmt)
            session.commit()
    except:
        # Todo: return error message
        return None

    # return author_id
    return result.inserted_primary_key[0]


def get_author(author_id=None, Session=Session):
    # return all if author_id is None

    stmt = select(author_table)

    if author_id is not None:
        stmt = stmt.where(author_table.c.author_id == author_id)

    try:
        with Session() as session:
            result = session.execute(stmt).all()
    except:
        # Todo: return error message
        return None

    # [(author_id, author_name)]
    return [i._asdict() for i in result]


def create_publisher(publisher_name, Session=Session):
    stmt = insert(publisher_table).values(
        publisher_name=publisher_name,
    )

    try:
        with Session() as session:
            result = session.execute(stmt)
            session.commit()
    except:
        # Todo: return error message
        return None

    # return publisher_id
    return result.inserted_primary_key[0]


def get_publisher(publisher_id=None, Session=Session):
    # return all if publisher_id is None

    stmt = select(publisher_table)

    if publisher_id is not None:
        stmt = stmt.where(publisher_table.c.publisher_id == publisher_id)

    try:
        with Session() as session:
            result = session.execute(stmt).all()
    except:
        # Todo: return error message
        return None

    # [(publisher_id, publisher_name)]
    return [i._asdict() for i in result]


def create_book_title(book_name, genre_id, Session=Session):

    stmt = insert(book_title_table).values(book_name=book_name, genre_id=genre_id)

    try:
        with Session() as session:
            result = session.execute(stmt)
            session.commit()
    except:
        # Todo: return error message
        return None

    # return book_title_id
    return result.inserted_primary_key[0]


def get_book_title(book_title_id=None, Session=Session):
    # return all if book_title_id is None

    stmt = select(book_title_table, book_genre_table.c.genre_name).join(
        book_genre_table
    )

    if book_title_id is not None:
        stmt = stmt.where(book_title_table.c.book_title_id == book_title_id)

    try:
        with Session() as session:
            result = session.execute(stmt).all()
    except:
        # Todo: return error message
        return None

    # [(book_title_id, book_name, genre_id)]
    return [i._asdict() for i in result]


def add_authors_to_book(book_title_id, author_ids, Session=Session):

    try:
        with Session() as session:
            result = session.execute(
                insert(book_author_list),
                [{"book_title_id": book_title_id, "author_id": i} for i in author_ids],
            )
            session.commit()
    except:
        # Todo: return error message
        return False

    return True


def create_book(book_title_id, publication_year, publisher_id, price, Session=Session):

    stmt = insert(book_table).values(
        book_title_id=book_title_id,
        publication_year=publication_year,
        publisher_id=publisher_id,
        price=price,
    )

    try:
        with Session() as session:
            result = session.execute(stmt)
            session.commit()
    except:
        # Todo: return error message
        return None

    # return book_id
    return result.inserted_primary_key[0]


def get_book(book_id=None, Session=Session):
    # return all if book_title_id is None

    stmt = (
        select(book_table, book_title_table)
        .join(book_title_table)
        .join(publisher_table)
    )

    if book_id is not None:
        stmt = stmt.filter(book_table.c.book_id.in_(book_id))

    try:
        with Session() as session:
            result = session.execute(stmt).all()
    except:
        # Todo: return error message
        return None

    return [i._asdict() for i in result]


def add_book_to_receipt(book_receipt_id, book_ids, quantities, Session=Session):

    try:
        with Session() as session:
            result = session.execute(
                insert(book_receipt_detail_table),
                [
                    {"book_receipt_id": book_receipt_id, "book_id": i, "quantity": q}
                    for i, q in zip(book_ids, quantities)
                ],
            )
            session.commit()
    except:
        # Todo: return error message
        return False

    return True


def create_book_receipt(book_ids=[], quantities=[], Session=Session):
    assert len(book_ids) == len(quantities)

    stmt = insert(book_receipt_table)
    try:
        with Session() as session:
            book_receipt_id = session.execute(stmt).inserted_primary_key[0]

            if book_receipt_id is None:
                session.rollback()
                return None

            if book_ids is not None and len(book_ids) > 0:
                session.execute(
                    insert(book_receipt_detail_table),
                    [
                        {
                            "book_receipt_id": book_receipt_id,
                            "book_id": i,
                            "quantity": q,
                        }
                        for i, q in zip(book_ids, quantities)
                    ],
                )
            session.commit()
    except:
        # Todo: return error message
        return None

    return book_receipt_id


def get_book_receipt(book_receipt_id=None, Session=Session):
    # return all if book_receipt_id is None

    stmt = select(
        book_receipt_table, book_receipt_detail_table.c["book_id", "quantity"]
    ).join(book_receipt_detail_table)

    if book_receipt_id is not None:
        stmt = stmt.where(book_receipt_table.c.book_receipt_id == book_receipt_id)

    try:
        with Session() as session:
            result = session.execute(stmt).all()
    except:
        # Todo: return error message
        return None

    return [i._asdict() for i in result]
