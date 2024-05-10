from flask import Blueprint
from flask import request

from src.database import USER

user_api = Blueprint("user_api", __name__)
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request

@user_api.route("/get", methods=["GET"])
def get_user():
    user_id = request.args.get("id")
    return USER.get_user(user_id=user_id)


@user_api.route("/create", methods=["POST"])
def create_user():
    email = request.form.get("email")
    password = request.form.get("password")
    reader_type_id = request.form.get("password")

    return USER.create_user(
        email=email, password=password, reader_type_id=reader_type_id
    )
