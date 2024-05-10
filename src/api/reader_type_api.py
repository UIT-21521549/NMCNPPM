from flask import Blueprint
from flask import request

from src.database import USER

reader_type_api = Blueprint("reader_type_api", __name__)


@reader_type_api.route("/get", methods=["GET"])
def get_reader_type():
    reader_type_id = request.args.get("id")
    return USER


@reader_type_api.route("/create", methods=["POST"])
def create_reader_type():
    reader_type = request.form.get("reader_type")
    return USER.create_reader_type(reader_type=reader_type)

