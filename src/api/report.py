from flask import Blueprint
from flask import request, make_response
from flask import jsonify
from src.database import REPORT

report_api = Blueprint("report", __name__, url_prefix="/report")

@report_api.route("/get_genre", methods=["POST"])
def get_genre(time):

    # Lấy tháng và năm từ tham số thời gian
    month = time.month
    year = time.year

    # Gọi hàm để lấy dữ liệu từ REPORT
    result = REPORT.get_rgt(month, year)

    # Tính tổng số lượng genre_id
    total = sum(result.values())

    # Tính phần trăm của mỗi genre_id
    percentages = {key: (value / total) * 100 for key, value in result.items()}

    return jsonify(percentages)



