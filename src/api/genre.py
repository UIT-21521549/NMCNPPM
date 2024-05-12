from flask import Blueprint
from flask import request
from flask import g
from src.helpers.auth import auth_decorator

from src.database import BOOK, Session

genre_api = Blueprint("genre", __name__, url_prefix="/genre")

@genre_api.route("/get_one", methods=["GET"])
def get_one():
    genre_id = request.args.get("id")
    if genre_id is None:
        return "id required", 400
    
    try:
        with Session() as session:
            rd = BOOK.get_genre(genre_id, session=session)
    except:
        return "genre not found", 400

    return rd[0]

@genre_api.route("/get_all", methods=["GET"])
def get_all():
    try:
        with Session() as session:
            result = BOOK.get_genre(session=session)
    except:
        return "genre not found", 500
    
    return result

@genre_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create():
    data = request.get_json(force=True)

    for k in ["genre_name"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = BOOK.create_genre(genre_name=data["genre_name"], session=session)
            session.commit()
    except:
        return "create genre fail", 400
        
    return {
        "genre_id": idx 
    }

