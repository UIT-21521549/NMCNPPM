from flask import Blueprint
from flask import request
from flask import g
from src.helpers.auth import auth_decorator

from src.database import BOOK, Session

book_api = Blueprint("book", __name__, url_prefix="/book")


@book_api.route("/get_one", methods=["GET"])
def get_one():
    book_id = request.args.get("id")
    if book_id is None:
        return "id required", 400
    try:
        with Session() as session:
            re = BOOK.get_book([book_id], session=session)
    except:
        return "book not found", 400

    return re[0]


@book_api.route("/get_all", methods=["GET"])
def get_all():
    
    try:
        with Session() as session:
            result = BOOK.get_book(session=session)
    except:
        return "book not found", 500

    return result


@book_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create():
    data = request.get_json(force=True)

    for k in ["book_title_id", "publication_year", "publisher_id", "price"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = BOOK.create_book(
                book_title_id=data["book_title_id"],
                publication_year=data["publication_year"],
                publisher_id=data["publisher_id"],
                price=data["price"],
                session=session
            )
            session.commit()
    except:
        return "book creation failed", 400

    return {"book_id": idx}
