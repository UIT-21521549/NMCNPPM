from flask import Blueprint
from flask import request

from src.database import BOOK

book_api = Blueprint("book", __name__, url_prefix="/book")


@book_api.route("/get_one", methods=["GET"])
def get_one():
    book_id = request.args.get("id")
    if book_id is None:
        return "id required", 400

    re = BOOK.get_book([book_id])

    if re is None or len(re) == 0:
        return "book not found", 400

    return re[0]


@book_api.route("/get_all", methods=["GET"])
def get_all():
    result = BOOK.get_book()

    if result is None:
        return "server error", 500

    return result


@book_api.route("/create", methods=["POST"])
def create():
    data = request.get_json(force=True)

    for k in ["book_title_id", "publication_year", "publisher_id", "price"]:
        if k not in data.keys():
            return f"{k} needed", 400

    idx = BOOK.create_book(
        book_title_id=data["book_title_id"],
        publication_year=data["publication_year"],
        publisher_id=data["publisher_id"],
        price=data["price"],
    )

    if idx is None:
        return "book already exists", 400
    return {"book_id": idx}
