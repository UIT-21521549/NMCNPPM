from flask import Blueprint
from flask import request

from src.database import BOOK

publisher_api = Blueprint("publisher", __name__, url_prefix="/publisher")

@publisher_api.route("/get_one", methods=["GET"])
def get_one():
    publisher_id = request.args.get("id")
    if publisher_id is None:
        return "id required", 400
    
    re = BOOK.get_publisher(publisher_id)

    if re is None or len(re) == 0:
        return "publisher not found", 400

    return re[0]

@publisher_api.route("/get_all", methods=["GET"])
def get_all():
    result = BOOK.get_publisher()

    if result is None or len(result) == 0:
        return "server error", 500
    
    return result

@publisher_api.route("/create", methods=["POST"])
def create():
    data = request.get_json(force=True)

    for k in ["publisher_name"]:
        if k not in data.keys():
            return f"{k} needed", 400

    idx = BOOK.create_publisher(publisher_name=data["publisher_name"])

    if idx is None:
        return "publisher already exists", 400
    return {
        "publisher_id": idx 
    }

