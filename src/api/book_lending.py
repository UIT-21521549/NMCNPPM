from flask import Blueprint
from flask import request

from flask import g
from src.helpers.auth import auth_decorator

from src.database import LENDING, Session

lending_api = Blueprint("book_lending", __name__, url_prefix="/lending")


@lending_api.route("/get_one", methods=["GET"])
@auth_decorator()
def get_one():
    lending_id = request.args.get("id")

    if lending_id is None:
        return "id required", 400

    try:
        with Session() as session:
            re = LENDING.get_lending([lending_id], session=session)
    except:
        return "lending_id not found", 400

    return re[0]


@lending_api.route("/get_by_user", methods=["GET"])
@auth_decorator()
def get_by_user_id():
    user_id = request.args.get("id")

    if user_id is None:
        return "user id required", 400

    try:
        with Session() as session:
            re = LENDING.get_lending_by_user_id(user_id, session=session)
    except:
        return "lending_id not found", 400

    return re


@lending_api.route("/get_current_user", methods=["GET"])
@auth_decorator()
def get_by_current_user_id():
    user_id = g.user_id

    try:
        with Session() as session:
            re = LENDING.get_lending_by_user_id(user_id, session=session)
    except:
        return "lending_id not found", 400

    return re

@lending_api.route("/get_all", methods=["GET"])
@auth_decorator(admin_only=True)
def get_all():

    try:
        with Session() as session:
            result = LENDING.get_lending(session=session)
    except:
        return "server error", 500

    return result


@lending_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create():
    data = request.get_json(force=True)

    for k in ["book_ids", "quantities", "user_id"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            idx = LENDING.create_book_lending(
                user_id=data["user_id"],
                book_ids=data["book_ids"],
                quantities=data["quantities"],
                session=session
            )
            session.commit()
    except Exception as e:
        print(e)
        return "create lending failed", 400

    return {"lending_id": idx}


@lending_api.route("/return", methods=["POST"])
@auth_decorator(admin_only=True)
def return_lending():
    lending_id = request.args.get("id")

    if lending_id is None:
        return "lending_id required", 400

    try:
        with Session() as session:
            idx = LENDING.return_lending(
                lending_id=lending_id,
                session=session
            )
            session.commit()
    except Exception as e:
        print(e)
        return "return lending failed", 400

    return "done"