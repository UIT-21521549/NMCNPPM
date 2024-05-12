from flask import Blueprint

from .user import user_api
from .reader_type import reader_type_api
from .genre import genre_api
from .author import author_api
from .publisher import publisher_api
from .book_title import book_title_api
from .book import book_api
from .book_receipt import book_receipt_api
from .image import image_api

api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(user_api)

api.register_blueprint(reader_type_api)

api.register_blueprint(genre_api)

api.register_blueprint(author_api)

api.register_blueprint(publisher_api)

api.register_blueprint(book_title_api)

api.register_blueprint(book_api)

api.register_blueprint(book_receipt_api)

api.register_blueprint(image_api)