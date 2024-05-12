from flask import Blueprint
from flask import request, render_template, make_response, redirect
from src.database import USER

login_page = Blueprint("login", __name__, url_prefix="/")



@login_page.route("/login", methods=["GET"])
def get_login_page():
    
    # return login page here
    return render_template('index.html')

@login_page.route("/login", methods=["POST"])
def get_token():
    email = request.form.get('email')
    password = request.form.get('password')

    token = USER.create_jwt_token(
        email=email,
        password=password
    )

    if token == None:
        return redirect("/login")

    resp = make_response(redirect("/"))
    resp.set_cookie("session_token", token)

    return resp
