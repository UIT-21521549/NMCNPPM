from flask import Blueprint

from .user import user_api
from .reader_type import reader_type_api
from .genre import genre_api
from .author import author_api

api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(user_api)

api.register_blueprint(reader_type_api)

api.register_blueprint(genre_api)

api.register_blueprint(author_api)
