from flask import Blueprint
from flask import request

from flask import g
from src.helpers.auth import auth_decorator

from src.database import REPORT, Session

report_api = Blueprint("report", __name__, url_prefix="/report")


@report_api.route("/get_overdue_lending", methods=["GET"])
@auth_decorator(admin_only=True)
def get_overdue_lending():
    param = request.args

    for k in ["day", "month", "year"]:
        if k not in param.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            rd = REPORT.get_overdue_lending(
                day=int(param["day"]),
                month=param["month"],
                year=param["year"],
                session=session,
            )
    except Exception as e:
        print(e)
        return "no record found", 400

    return rd


@report_api.route("/get_per_genre_report", methods=["GET"])
@auth_decorator(admin_only=True)
def type_book():
    param = request.args

    for k in ["month", "year"]:
        if k not in param.keys():
            return f"{k} needed", 400

    try:
        with Session() as session:
            rd = REPORT.get_per_genre_report(
                month=param["month"], year=param["year"], session=session
            )
    except Exception as e:
        print(e)
        return "no record found", 400

    return rd
