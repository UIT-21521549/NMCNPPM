from flask import Blueprint
from flask import request
from flask import jsonify

from flask import g
from src.helpers.auth import auth_decorator

from src.database import USER, Session

user_api = Blueprint("user", __name__, url_prefix="/user")
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request


@user_api.route("/get_one", methods=["GET"])
def get_one():
    user_id = request.args.get("id")

    if user_id is None:
        return "id required", 400

    try:
        with Session() as session:
            users = USER.get_users(user_ids=[user_id], session=session)
    except:
        return "user not found", 400

    return users[0]


@user_api.route("/get_all", methods=["GET"])
def get_all():
    try:
        with Session() as session:
            users = USER.get_users(session=session)
    except:
        return "no user found", 500

    return users


@user_api.route("/create", methods=["POST"])
def create_user():
    data = request.get_json(force=True)

    for k in ["email", "password", "reader_type_id", "user_name", "birthday", "address"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            new_user_id = USER.create_user(
                email=data["email"],
                password=data["password"],
                # reader_type_id=data["reader_type_id"],
                session=session,
            )
            session.commit()
    except:
        return "user creation failed", 400

    return {"user_id": new_user_id}


@user_api.route("/get_auth_token", methods=["POST"])
def get_token():
    data = request.get_json(force=True)

    for k in ["email", "password"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            token = USER.create_jwt_token(
                email=data["email"], password=data["password"], session=session
            )
    except:
        return "authentication failed", 400

    return {"token": token}


@user_api.route("/get_by_token", methods=["GET"])
@auth_decorator()
def get_current():
    user_id = g.user_id
    is_admin = g.is_admin

    try:
        with Session() as session:
            info = USER.get_users([user_id], session=session)
    except:
        return "user not found", 400

    return info[0]
