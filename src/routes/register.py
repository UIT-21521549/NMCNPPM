from flask import Blueprint
from flask import request, render_template, make_response, redirect
from src.database import USER

register_page = Blueprint("register", __name__, url_prefix="/register")



@login_page.route("/", methods=["GET"])
def get_register_page():
    
    # return login page here
    return render_template('index.html')

@login_page.route("/", methods=["POST"])
def register():
    email = request.form.get('email')
    password = request.form.get('password')

