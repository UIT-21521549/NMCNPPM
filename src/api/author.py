from flask import Blueprint
from flask import request

from src.database import BOOK

author_api = Blueprint("author", __name__, url_prefix="/author")

@author_api.route("/get_one", methods=["GET"])
def get_one():
    author_id = request.args.get("id")
    if author_id is None:
        return "id required", 400
    
    re = BOOK.get_author(author_id)

    if re is None or len(re) == 0:
        return "author not found", 400

    return re[0]

@author_api.route("/get_all", methods=["GET"])
def get_all():
    result = BOOK.get_author()

    if result is None:
        return "server error", 500
    
    return result

@author_api.route("/create", methods=["POST"])
def create():
    data = request.get_json(force=True)

    for k in ["author_name"]:
        if k not in data.keys():
            return f"{k} needed", 400

    idx = BOOK.create_author(author_name=data["author_name"])

    if idx is None:
        return "author already exists", 400
    return {
        "author_id": idx 
    }

@author_api.route("/add_to_book_title", methods=["POST"])
def add_to_book():
    data = request.get_json(force=True)

    for k in ["book_title_id", "author_ids"]:
        if k not in data.keys():
            return f"{k} needed", 400

    re = BOOK.add_authors_to_book(book_title_id=data["book_title_id"], author_ids=data["author_ids"])

    if re:
        return "done!"
    else:
        return "errors", 400
