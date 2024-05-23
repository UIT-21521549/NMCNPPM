from flask import Blueprint
from flask import request
from flask import g
from src.helpers.auth import auth_decorator
from src.database import BOOK, Session

publisher_api = Blueprint("publisher", __name__, url_prefix="/publisher")

@publisher_api.route("/get_one", methods=["GET"])
def get_one():
    publisher_id = request.args.get("id")
    if publisher_id is None:
        return "id required", 400
        
    try:
        with Session() as session:
            re = BOOK.get_publisher(publisher_id, session=session)
    except:
        return "publisher not found", 400

    return re[0]

@publisher_api.route("/get_all", methods=["GET"])
def get_all():
    try:
        with Session() as session:
            re = BOOK.get_publisher(session=session)
    except:
        return "publisher not found", 500

    return re

@publisher_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create():
    data = request.get_json(force=True)

    for k in ["publisher_name"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = BOOK.create_publisher(publisher_name=data["publisher_name"], session=session)
            session.commit()
    except:
        return "create publisher failed", 400
    
    return {
        "publisher_id": idx 
    }



@publisher_api.route("/change_name", methods=["POST"])
@auth_decorator(admin_only=True)
def change_name():
    data = request.get_json(force=True)

    for k in ["new_publisher_name", "publisher_id"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = BOOK.change_publisher_name(
                publisher_id=data["publisher_id"],
                new_publisher_name=data["new_publisher_name"],
                session=session,
            )
            session.commit()
    except:
        return "change publisher name fail", 400

    return "success!"