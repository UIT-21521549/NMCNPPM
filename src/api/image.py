from flask import Blueprint, send_file
from flask import request
from flask import g
from src.helpers.auth import auth_decorator
from src.helpers.image import save_image
import os
from src.database import IMAGE, Session

image_api = Blueprint("image", __name__, url_prefix="/image")

default_book_images = os.getenv("default_book_images")


@image_api.route("/get", methods=["GET"])
def get_one():
    image_id = request.args.get("id")
    if image_id is None:
        return send_file(default_book_images, mimetype='image/gif')

    try:
        with Session() as session:
            re = IMAGE.get_image(image_id, session=session)
    except:
        return "image not found", 400
    
    img_path = re["file_path"]

    return send_file(img_path, mimetype='image/gif')

@image_api.route("/delete", methods=["DELETE"])
def del_one():
    image_id = request.args.get("id")

    if image_id is None:
        return "id required", 400

    try:
        with Session() as session:
            IMAGE.remove_images([image_id], session=session)
            session.commit()
    except Exception as e:
        print(e)
        return "image not found", 400

    return "done"

@image_api.route("/add_to_book_title", methods=["POST"])
def add_to_book():
    book_title_id = request.args.get("id")

    if book_title_id is None:
        return "book_title_id required", 400

    if "file" not in request.files.keys():
        return "image file needed", 400


    try:
        with Session() as session:
            img_file = request.files["file"]

            output_path, file_name = save_image(img_file)

            re = IMAGE.add_image_to_book_title(
                book_title_id=book_title_id,
                image_file_name=file_name,
                file_path=output_path,
                session=session,
            )
            session.commit()
            IMAGE.remove_orphaned_images(session)
            session.commit()
    except Exception as e:
        print(e)
        try:
            os.remove(output_path)
        except OSError:
            pass

        return "saving image failed", 400

    return {
        "image_id": re
    }
