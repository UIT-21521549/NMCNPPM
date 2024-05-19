import os
from .connection import Session, create_new
import src.database.book as BOOK
import src.database.user as USER
import src.database.lending as LENDING
import random, string


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def random_suffix(length):
    letters = "0123456789"
    return "".join(random.choice(letters) for i in range(length))


def set_up(session):

    for rt in ["X", "Y"]:
        USER.create_reader_type(reader_type=rt, session=session)

    USER.create_user(
        email="abc1",
        password="abc1",
        reader_type_id=random.randrange(1, 3),
        user_name=randomword(15),
        session=session,
    )

    for i in range(10):
        USER.create_user(
            email=random_suffix(8),
            password=random_suffix(8),
            reader_type_id=random.randrange(1, 3),
            user_name=randomword(15),
            session=session,
        )

    for i in range(10):
        BOOK.create_genre(f"genre{random_suffix(4)}", session=session)

        BOOK.create_author(f"author{random_suffix(4)}", session=session)

        BOOK.create_publisher(f"publisher{random_suffix(4)}", session=session)

    for i in range(20):
        b_id = BOOK.create_book_title(
            book_name=f"book_title{random_suffix(4)}",
            genre_id=random.randrange(1, 11),
            session=session,
        )

        BOOK.add_authors_to_book(
            book_title_id=b_id,
            author_ids=random.sample(range(1, 11), random.randrange(1, 4)),
            session=session,
        )

    for i in range(30):
        BOOK.create_book(
            book_title_id=random.randrange(1, 21),
            publication_year=random.randrange(1900, 2050),
            publisher_id=random.randrange(1, 11),
            price=random.randrange(10, 100),
            session=session,
        )

        BOOK.create_book_receipt(
            book_ids=[i + 1],
            quantities=[random.randrange(1, 30)],
            session=session,
        )

    for i in range(15):
        no_b = random.randrange(1, 5)

        BOOK.create_book_receipt(
            book_ids=random.sample(range(1, 31), no_b),
            quantities=[random.randrange(1, 20) for _ in range(no_b)],
            session=session,
        )

    for i in range(2, 10):
        no_b = random.randrange(1, 3)
        LENDING.create_book_lending(
            user_id=i,
            book_ids=random.sample(range(1, 31), no_b),
            quantities=[random.randrange(1, 3) for _ in range(no_b)],
            session=session,
        )

    for i in range(1, 7):
        LENDING.return_lending(lending_id=i, session=session)

    for j in range(3):
        USER.pay_penalty(
            user_id=2,
            amount=30,
            session=session
        )
