<<<<<<< HEAD
from flask import Blueprint
from flask import request

from flask import g
from src.helpers.auth import auth_decorator

from src.database import REPORT, Session

report_api = Blueprint("report", __name__, url_prefix="/report")


@report_api.route("/get_overdue_lending", methods=["GET"])
def get_overdue_lending():
    data = request.get_json(force=True)

    for k in ["day", "month", "year"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            rd = REPORT.get_overdue_lending(
                day=data["day"], month=data["month"], year=data["year"], session=session
            )
    except Exception as e:
        print(e)
        return "no record found", 400

    return rd


@report_api.route("/type_book", methods=["POST"])
def type_book():
    data = request.json  # Get data from the request body
    month = data.get('month')
    year = data.get('year')

    genre_counts = {}
    total_books = 0

    lendings = LENDING.get_lending(session=Session)

    for row in lendings:
        lending_date = row.get("lending_date")
        if int(year) == lending_date.year and int(month) == lending_date.month:
            items = row["items"]  # Access "items" directly
            book_ids = [item["book_id"] for item in items]  # Extract book IDs from items
            results = BOOK.get_book(book_ids=book_ids, session=Session)
            for book in results:
                genre_id = book["genre_id"]
                genre_name = book["genre_name"]
                if genre_id in genre_counts:
                    genre_counts[genre_id]["sl"] += 1
                else:
                    genre_counts[genre_id] = {"genre_name": genre_name, "sl": 1}
                total_books += 1

    # Convert data to JSON format with book percentage
    json_data = []
    for key, value in genre_counts.items():
        percentage = (value["sl"] / total_books) * 100 if total_books > 0 else 0
        json_data.append({"genre_id": key, "genre_name": value["genre_name"], "percentage": percentage})

    return jsonify(json_data)
