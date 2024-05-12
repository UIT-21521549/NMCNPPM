from flask import Blueprint
from flask import request

from flask import g
from src.helpers.auth import auth_decorator

from src.database import USER, Session

reader_type_api = Blueprint("reader_type", __name__, url_prefix="/reader_type")

@reader_type_api.route("/get_one", methods=["GET"])
def get_reader_type():
    reader_type_id = request.args.get("id")

    if reader_type_id is None:
        return "reader_type_id required", 400
    
    try:
        with Session() as session:
            rd = USER.get_reader_type(reader_type_id, session=session)
    except:
        return "reader type found", 400

    return rd[0]

@reader_type_api.route("/get_all", methods=["GET"])
def get_all():
    try:
        with Session() as session:
            rd = USER.get_reader_type(session=session)
    except:
        return "server error", 500
    
    return rd

@reader_type_api.route("/create", methods=["POST"])
@auth_decorator(admin_only=True)
def create_reader_type():
    data = request.get_json(force=True)

    for k in ["reader_type"]:
        if k not in data.keys():
            return f"{k} needed", 400
    
    try:
        with Session() as session:
            idx = USER.create_reader_type(reader_type=data["reader_type"], session=session)
            session.commit()
    except:
        return "create reader_type failed", 400
        
    return {
        "reader_type_id": idx 
    }

