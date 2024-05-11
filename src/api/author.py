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

    if result is None or len(result) == 0:
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

