from flask import Blueprint
from flask import request

from src.database import BOOK

genre_api = Blueprint("genre", __name__, url_prefix="/genre")

@genre_api.route("/get_one", methods=["GET"])
def get_one():
    genre_id = request.args.get("id")
    if genre_id is None:
        return "id required", 400
    
    rd = BOOK.get_genre(genre_id)

    if rd is None or len(rd) == 0:
        return "genre not found", 400

    return rd[0]

@genre_api.route("/get_all", methods=["GET"])
def get_all():
    result = BOOK.get_genre()

    if result is None:
        return "server error", 500
    
    return result

@genre_api.route("/create", methods=["POST"])
def create():
    data = request.get_json(force=True)

    for k in ["genre_name"]:
        if k not in data.keys():
            return f"{k} needed", 400

    idx = BOOK.create_genre(genre_name=data["genre_name"])

    if idx is None:
        return "genre already exists", 400
    return {
        "genre_id": idx 
    }

