from sqlalchemy import event, DDL

from .models import *

update_book_quantities_on_insert_sqlite = DDL(
    """\
CREATE TRIGGER IF NOT EXISTS update_book_quantities_on_insert AFTER INSERT ON book_receipt_detail
BEGIN
    UPDATE book
    SET quantity = book_quant.total
    FROM
        (
            SELECT SUM(quantity) as total, book_id
            FROM book_receipt_detail
            GROUP BY book_id
        ) AS book_quant
    WHERE book.book_id = book_quant.book_id;
END"""
)

update_book_quantities_on_delete_sqlite = DDL(
    """\
CREATE TRIGGER IF NOT EXISTS update_book_quantities_on_delete AFTER DELETE ON book_receipt_detail
BEGIN
    UPDATE book
    SET quantity = book_quant.total
    FROM
        (
            SELECT SUM(quantity) as total, book_id
            FROM book_receipt_detail
            GROUP BY book_id
        ) AS book_quant
    WHERE book.book_id = book_quant.book_id;
END"""
)


update_book_quantities_on_update_sqlite = DDL(
    """\
CREATE TRIGGER IF NOT EXISTS update_book_quantities_on_update AFTER UPDATE OF quantity ON book_receipt_detail
BEGIN
    UPDATE book
    SET quantity = book_quant.total
    FROM
        (
            SELECT SUM(quantity) as total, book_id
            FROM book_receipt_detail
            GROUP BY book_id
        ) AS book_quant
    WHERE book.book_id = book_quant.book_id;
END"""
)

event.listen(
    book_receipt_detail_table,
    "after_create",
    update_book_quantities_on_insert_sqlite.execute_if(dialect="sqlite"),
)

event.listen(
    book_receipt_detail_table,
    "after_create",
    update_book_quantities_on_delete_sqlite.execute_if(dialect="sqlite"),
)

event.listen(
    book_receipt_detail_table,
    "after_create",
    update_book_quantities_on_update_sqlite.execute_if(dialect="sqlite"),
)
