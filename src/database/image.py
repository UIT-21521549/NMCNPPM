from sqlalchemy import select, insert, null, update, delete
from .connection import Session

from .models import image_table, book_title_table
import os


def get_image(image_id, session):
    stmt = select(image_table).where(image_table.c.image_id == image_id)

    result = session.execute(stmt).all()

    assert len(result) != 0

    return result[0]._asdict()


def add_image_to_book_title(book_title_id, image_file_name, file_path, session):

    add_image_stmt = insert(image_table).values(
        image_file_name=image_file_name, file_path=file_path
    )

    image_id = session.execute(add_image_stmt).inserted_primary_key[0]

    add_image_to_book_title_stmt = (
        update(book_title_table)
        .where(book_title_table.c.book_title_id == book_title_id)
        .values(image_id=image_id)
    )

    session.execute(add_image_to_book_title_stmt)

    return image_id


def remove_images(image_ids, session):

    # get image paths
    stmt = select(image_table.c.file_path).where(image_table.c.image_id.in_(image_ids))

    file_paths = [i._asdict()["file_path"] for i in session.execute(stmt).all()]

    assert len(file_paths) != 0

    stmt = delete(image_table).where(image_table.c.image_id.in_(image_ids))

    session.execute(stmt)

    for fp in file_paths:
        try:
            os.remove(fp)
        except OSError:
            pass

    return True


def remove_orphaned_images(session):

    stmt = select(image_table.c.image_id, book_title_table.c.book_title_id).join(
        book_title_table, isouter=True
    ).where(book_title_table.c.book_title_id == None)

    img_ids = [i._asdict()["image_id"] for i in session.execute(stmt).all()]

    if len(img_ids) == 0:
        return 
    remove_images(img_ids, session=session)