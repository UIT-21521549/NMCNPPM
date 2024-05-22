from sqlalchemy import select, insert, extract, null, desc, asc, update, and_, or_, func
from sqlalchemy.sql import text, func
from .models import book_title_table, lending_table, book_table, lending_detail_table, book_genre_table
from datetime import datetime, timezone, timedelta, date


def get_overdue_lending(day, month, year, session=None):

    today = datetime(
        day=day,
        month=month,
        year=year,
    )

    stmt = (
        select(
            lending_table.c["user_id", "lending_date", "lending_id", "return_deadline"],
            book_table.c.book_id,
            book_title_table.c["book_name", "book_title_id"],
        )
        .select_from(lending_table)
        .join(lending_detail_table)
        .join(book_table)
        .join(book_title_table)
        .where(
            and_(
                or_(  # lendings that have not been returned
                    lending_table.c.return_date > today,
                    lending_table.c.return_date == None,
                ),
                lending_table.c.return_deadline <= today,
            )
        )
    )

    result = session.execute(stmt).all()

    result = [i._asdict() for i in result]

    for i in range(len(result)):
        num_day_late = (today - result[i]["return_deadline"]).days

        result[i]["num_day_late"] = num_day_late

    return result


def get_per_genre_report(month, year, session=None):

    sum1 = func.sum(lending_detail_table.c.quantity).label("total_lending")

    stmt = (
        select(sum1, book_genre_table.c["genre_id", "genre_name"])
        .select_from(lending_detail_table)
        .join(lending_table)
        .join(book_table)
        .join(book_title_table)
        .join(book_genre_table)
        .where(
            and_(
                extract("year", lending_table.c.lending_date) == year,
                extract("month", lending_table.c.lending_date) == month,
            )
        )
        .group_by(book_genre_table.c["genre_id", "genre_name"])
    )

    result = session.execute(stmt).all()

    result = [i._asdict() for i in result]

    total = sum([i["total_lending"] for i in result])

    for i in range(len(result)):
        if total == 0:
            return result
        result[i]["ratio"] = result[i]["total_lending"] / total

    return result
