from flask import Blueprint
from .login import login_page

routes = Blueprint("routes", __name__, url_prefix="/")

routes.register_blueprint(login_page)
