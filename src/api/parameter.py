from flask import Blueprint
from flask import request, make_response

from flask import g
from src.helpers.auth import auth_decorator

from src.database import PARAM, Session

param_api = Blueprint("parameter", __name__, url_prefix="/param")


@param_api.route("/get", methods=["GET"])
@auth_decorator(admin_only=True)
def get_one():
    try:
        with Session() as session:
            param = PARAM.get_parameter(session=session)
    except:
        return "no parameter found", 400

    return param

@param_api.route("/set", methods=["POST"])
@auth_decorator(admin_only=True)
def set_param():
    data = request.get_json(force=True)

    for k in ["param_name", "new_value"]:
        if k not in data.keys():
            return f"{k} needed", 400
        
    try:
        with Session() as session:

            PARAM.set_param(
                param_name=data["param_name"],
                new_value=data["new_value"],
                session=session
            )
            session.commit()
    except Exception as e:
        print(e)
        return "update parameters failed", 400
    
    return "done!"