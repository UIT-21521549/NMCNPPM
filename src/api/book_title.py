from flask import Blueprint
from flask import request
from flask import g
from src.helpers.auth import auth_decorator
from src.database import BOOK, Session

book_title_api = Blueprint("book_title", __name__, url_prefix="/book_title")


@book_title_api.route("/get_one", methods=["GET"])
def get_one():
    book_title_id = request.args.get("id")

    if book_title_id is None:
        return "id required", 400

    try:
        with Session() as session:
            re = BOOK.get_book_title([book_title_id], session=session)
    except Exception as e:
        print(e)
        return "book_title not found", 400

    return re[0]

@book_title_api.route("/get_many", methods=["GET"])
def get_many():
    data = request.get_json(force=True)

    for k in ["book_title_ids"]:
        if k not in data.keys():
            return f"{k} needed", 400

    book_title_ids = data["book_title_ids"]

    try:
        with Session() as session:
            re = BOOK.get_book_title(book_title_ids, session=session)
    except Exception as e:
        print(e)
        return "book_title not found", 400

    return re

@book_title_api.route("/get_all", methods=["GET"])
def get_all():

    try:
        with Session() as session:
            result = BOOK.get_book_title(session=session)
    except:
        return "book_title not found", 500

    return result

@book_title_api.route("/get_detail", methods=["GET"])
def get_detail():
    book_title_id = request.args.get("id")

    if book_title_id is None:
        return "id required", 400

    try:
        with Session() as session:
            result = BOOK.get_book_title_details(book_title_id, session=session)
    except Exception as e:
        return "book_title not found", 500

    return result

@book_title_api.route("/get_new_books", methods=["GET"])
def get_new_books():
    n = request.args.get("n")

    if n is None:
        n = 4

    try:
        with Session() as session:
            result = BOOK.get_n_newly_added_book_title(n, session=session)
    except Exception as e:
        print(e)
        return "cannot get new books", 500

    return result

@book_title_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create():
    data = request.get_json(force=True)

    for k in ["book_name", "genre_id"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = BOOK.create_book_title(
                book_name=data["book_name"], genre_id=data["genre_id"], session=session
            )
            session.commit()
    except:
        return "create book_title fail", 400

    return {"book_title_id": idx}
