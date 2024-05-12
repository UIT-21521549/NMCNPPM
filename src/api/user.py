from flask import Blueprint
from flask import request
from flask import jsonify


from src.database import USER

user_api = Blueprint("user", __name__, url_prefix="/user")
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request

@user_api.route("/get_one", methods=["GET"])
def get_one():
    user_id = request.args.get("id")

    if user_id is None:
        return "id required", 400

    users = USER.get_users(user_ids=[user_id])

    if users is None or len(users) == 0:
        return "user not found", 400
    
    return users[0]

@user_api.route("/get_all", methods=["GET"])
def get_all():
    users = USER.get_users()

    if users is None:
        return "server error", 500
    
    return users


@user_api.route("/create", methods=["POST"])
def create_user():
    data = request.get_json(force=True)

    for k in ["email", "password", "reader_type_id"]:
        if k not in data.keys():
            return f"{k} needed", 400
    
    new_user_id = USER.create_user(
        email=data["email"], password=data["password"], reader_type_id=data["reader_type_id"]
    )

    if new_user_id is None:
        return "user already exists", 400

    return {
        "user_id": new_user_id 
    }

@user_api.route("/get_auth_token", methods=["POST"])
def get_token():
    data = request.get_json(force=True)

    for k in ["email", "password"]:
        if k not in data.keys():
            return f"{k} needed", 400
    
    token = USER.create_jwt_token(
        email=data["email"],
        password=data["password"]
    )

    if token is None:
        return "authentication failed", 400

    return {
        "token": token
    }


@user_api.route("/get_by_token", methods=["GET"])
def get_current():
    token = request.cookies.get("session_token")

    if token is None:
        data = request.get_json(force=True)
        if "session_token" not in data.keys():
            return "session_token needed", 400

        token = data["session_token"]
    
    info = USER.verify_jwt_token(token)

    if info is None:
        return "token expired!", 400
    
    return info
        

    

