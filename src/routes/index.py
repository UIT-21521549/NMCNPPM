from flask import Blueprint
from flask import request, render_template, make_response, redirect
from src.database import USER

index_page = Blueprint("index", __name__, url_prefix="")


@index_page.route("", methods=["GET"])
def get_index_page():
    
    # return index page here
    return render_template('index.html')