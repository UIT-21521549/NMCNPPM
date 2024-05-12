from flask import Blueprint
from flask import request, render_template, make_response, redirect
from src.database import USER

login_page = Blueprint("login", __name__, url_prefix="/login")



@login_page.route("", methods=["GET"])
def get_login_page():
    
    # return login page here
    return render_template('index.html')

@login_page.route("", methods=["POST"])
def get_token():
    data = request.get_json(force=True)

    for k in ["email", "password"]:
        if k not in data.keys():
            return f"{k} needed", 400
        if len(data[k]) == 0:
            return f"{k} needed", 400

    email = data.get('email')
    password = request.form.get('password')
    # reader_type_id=request.form.get('reader_type_id')
    
    token = USER.create_jwt_token(
        email=data["email"],
        password=data["password"]
    )

    resp = make_response()

    if token == None:
        return resp

    resp.set_cookie("session_token", token)

    return resp
