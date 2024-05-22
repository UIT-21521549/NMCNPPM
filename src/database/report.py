from sqlalchemy import select, insert, null, desc, asc, update, and_, or_, func
from sqlalchemy.sql import text
from .models import book_title_table, lending_table, book_table, lending_detail_table
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

