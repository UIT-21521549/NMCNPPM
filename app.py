from argparse import ArgumentParser
from dotenv import load_dotenv

parser = ArgumentParser()
parser.add_argument("--config", type=str, default="./configs/example.env")
args = parser.parse_args()

# IMPORTANT: this need to be run before all other imports
load_dotenv(args.config)
# only import other class after this

from flask import Flask, request, render_template, redirect, make_response
from src.database import user


app = Flask(__name__)


@app.route("/")
def login():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login_check():

    session_token = request.cookies.get("session_token")
    # TODO: verify session_token
    if session_token:
        # already logged in
        return redirect("index.html")

    username = request.form.get("username")
    password = request.form.get("password")

    token = user.get_jwt_token(username, password)

    if token == None:
        return redirect("/login")

    resp = make_response(render_template(index.html))
    resp.set_cookie("session_token", token)

    return resp


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    result = user.register(username, password)

    if result:
        return redirect("/login")

    return render_template("register.html")


@app.route("/home")
def home():
    # return response for /home page
    pass


if __name__ == "__main__":
    app.run(debug=True)
