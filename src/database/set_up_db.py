import os
from .connection import Session, create_new
import src.database.book as BOOK
import src.database.user as USER
import random, string


def randomword(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def random_suffix(length):
    letters = "0123456789"
    return "".join(random.choice(letters) for i in range(length))


def set_up():
    # create admin user
    admin_password = os.getenv("admin_password")

    USER.create_user(
        email="admin@admin", password=admin_password, user_name="admin", is_admin=True
    )

    for rt in ["X", "Y"]:
        USER.create_reader_type(reader_type=rt)

    for i in range(4):
        USER.create_user(
            email=random_suffix(8),
            password=random_suffix(8),
            reader_type_id=random.randrange(1, 3),
            user_name=random_suffix(8),
        )

    for i in range(10):
        BOOK.create_genre(f"genre{random_suffix(3)}")

        BOOK.create_author(f"author{random_suffix(3)}")

        BOOK.create_publisher(f"publisher{random_suffix(3)}")

    for i in range(20):
        b_id = BOOK.create_book_title(
            book_name=f"book_title{random_suffix(5)}", genre_id=random.randrange(1, 11)
        )

        BOOK.add_authors_to_book(
            book_title_id=b_id,
            author_ids=random.sample(range(1, 11), random.randrange(1, 4)),
        )

    for i in range(30):
        BOOK.create_book(
            book_title_id=random.randrange(1, 21),
            publication_year=random.randrange(1900, 2050),
            publisher_id=random.randrange(1, 11),
            price=random.randrange(10, 100),
        )

    for i in range(15):
        no_b = random.randrange(1, 5)

        BOOK.create_book_receipt(
            book_ids=random.sample(range(1, 31), no_b),
            quantities=[random.randrange(1, 20) for _ in range(no_b)],
        )

    # TODO add dummy data
