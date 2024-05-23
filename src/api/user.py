from flask import Blueprint
from flask import request, make_response
from flask import jsonify

from flask import g
from src.helpers.auth import auth_decorator

from src.database import USER, Session, LENDING

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

@user_api.route("delete_one", methods=["DELETE"])
def delete_one():
    user_id = request.args.get("id")
    if not user_id:
        return jsonify({"error": u"Thiếu ID người dùng"}), 400

    with Session() as session:
        er = LENDING.get_lending_by_user_id(user_id=user_id, session=session)
        if er:
            return jsonify({"error": u"Không thể xóa"}), 404
        
        USER.delete_user(user_id=user_id, session=session)
        session.commit()
        return jsonify({"message": u"Xóa thành công"}), 200



@user_api.route("/get_by_email", methods=["GET"])
def get_by_email():
    data = request.get_json(force=True)

    for k in ["email"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            users = USER.get_user_by_email(user_email=data["email"], session=session)
    except Exception as e:
        return "email not found", 400

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

    for k in [
        "email",
        "password",
        "reader_type_id",
        "user_name",
        "birthday",
        "address",
    ]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            new_user_id = USER.create_user(
                email=data["email"],
                password=data["password"],
                reader_type_id=data["reader_type_id"],
                user_name=data["user_name"],
                birthday=data["birthday"],
                address=data["address"],
                session=session,
            )
            session.commit()
    except Exception as e:
        print(e)
        return "user creation failed", 400

    return {"user_id": new_user_id}


@user_api.route("/get_auth_token", methods=["POST"])
@auth_decorator(logged_in_required=False)
def get_token():
    if g.logged_in:
        return "you are already logged in!", 400

    data = request.get_json(force=True)

    for k in ["email", "password"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            result = USER.create_jwt_token(
                email=data["email"], password=data["password"], session=session
            )
    except Exception as e:
        print(e)
        return "authentication failed", 400

    resp = make_response(result)

    resp.set_cookie("session_token", result["token"])

    return resp


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


@user_api.route("/logout", methods=["GET"])
@auth_decorator()
def log_out():
    resp = make_response("logout")

    resp.delete_cookie("session_token")

    return resp


@user_api.route("/pay_penalty", methods=["POST"])
@auth_decorator(admin_only=True)
def pay_penalty():
    data = request.get_json(force=True)

    for k in ["user_id", "amount"]:
        if k not in data.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            result = USER.pay_penalty(
                user_id=data["user_id"], amount=data["amount"], session=session
            )
            session.commit()
    except Exception as e:
        return "pay penalty failed", 400

    return "done"


# @user_api.route("/pay_penalty", methods=["POST"])
# @auth_decorator(admin_only=True)
# def get_penalty():
#     publisher_id = request.args.get("id")
