from flask import Blueprint
from flask import request
from flask import g
from src.helpers.auth import auth_decorator
from src.database import BOOK

book_title_api = Blueprint("book_title", __name__, url_prefix="/book_title")

@book_title_api.route("/get_one", methods=["GET"])
def get_one():
    book_title_id = request.args.get("id")
    if book_title_id is None:
        return "id required", 400
    
    re = BOOK.get_book_title(book_title_id)

    if re is None or len(re) == 0:
        return "book_title not found", 400

    return re[0]

@book_title_api.route("/get_all", methods=["GET"])
def get_all():
    result = BOOK.get_book_title()

    if result is None:
        return "server error", 500
    
    return result

@book_title_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create():
    data = request.get_json(force=True)

    for k in ["book_name", "genre_id"]:
        if k not in data.keys():
            return f"{k} needed", 400

    idx = BOOK.create_book_title(book_name=data["book_name"], genre_id=data["genre_id"])

    if idx is None:
        return "book_title already exists", 400
    return {
        "book_title_id": idx 
    }

