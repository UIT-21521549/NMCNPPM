from flask import Blueprint
from flask import request

from src.database import BOOK, Session
from flask import g
from src.helpers.auth import auth_decorator

author_api = Blueprint("author", __name__, url_prefix="/author")


@author_api.route("/get_one", methods=["GET"])
def get_one():
    author_id = request.args.get("id")
    if author_id is None:
        return "id required", 400

    try:
        with Session() as session:
            re = BOOK.get_author(author_id, session=session)
    except:
        return "author not found", 400

    return re[0]


@author_api.route("/get_all", methods=["GET"])
def get_all():

    try:
        with Session() as session:
            result = BOOK.get_author(session=session)
    except:
        return "server error", 500

    return result


@author_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create():
    data = request.get_json(force=True)

    for k in ["author_name"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = BOOK.create_author(author_name=data["author_name"], session=session)
            session.commit()
    except:
        return "create author failed", 400

    return {"author_id": idx}


@author_api.route("/add_to_book_title", methods=["POST"])
@auth_decorator(admin_only=True)
def add_to_book():
    data = request.get_json(force=True)

    for k in ["book_title_id", "author_ids"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            BOOK.add_authors_to_book(
                book_title_id=data["book_title_id"],
                author_ids=data["author_ids"],
                session=session,
            )
            session.commit()

    except:
        return "errors", 400

    return "done!"


@author_api.route("/change_name", methods=["POST"])
@auth_decorator(admin_only=True)
def change_name():
    data = request.get_json(force=True)

    for k in ["new_author_name", "author_id"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = BOOK.change_author_name(
                author_id=data["author_id"],
                new_author_name=data["new_author_name"],
                session=session,
            )
            session.commit()
    except:
        return "change author name fail", 400

    return "success!"

