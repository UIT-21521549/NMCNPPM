from flask import Blueprint
from flask import request

from flask import g
from src.helpers.auth import auth_decorator

from src.database import BOOK, Session

book_receipt_api = Blueprint("book_receipt", __name__, url_prefix="/book_receipt")


@book_receipt_api.route("/get_one", methods=["GET"])
def get_one():
    book_receipt_id = request.args.get("id")

    if book_receipt_id is None:
        return "id required", 400

    try:
        with Session() as session:
            re = BOOK.get_book_receipt(book_receipt_id, session=session)
    except:
        return "book_receipt not found", 400

    return re[0]


@book_receipt_api.route("/get_all", methods=["GET"])
def get_all():

    try:
        with Session() as session:
            result = BOOK.get_book_receipt(session=session)
    except:
        return "server error", 500

    return result


@book_receipt_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create():
    data = request.get_json(force=True)

    for k in ["book_ids", "quantities"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = BOOK.create_book_receipt(
                book_ids=data["book_ids"],
                quantities=data["quantities"],
                session=session
            )
            session.commit()
    except:
        return "create book_receipt fail", 400

    return {"book_receipt_id": idx}
