from PIL import Image
from io import BytesIO
import hashlib
import os

images_save_path = os.getenv("images_upload_dir")

if images_save_path is None:
    images_save_path = "./images_upload"

def save_image(img_file, output_dir=images_save_path):
    file_name = img_file.filename

    img = Image.open(img_file.stream)

    width, height = img.size
    ratio = width/height

    # target res is 500 * 750
    if ratio >= 1: # wide image
        new_width = min(500, width)
        new_height = int(new_width/ratio)
    else: # tall image
        new_height = min(750, height)
        new_width = int(new_height*ratio)
    
    img = img.resize((new_width, new_height), resample=Image.LANCZOS)

    img = img.convert('RGB')

    img_hash=hashlib.sha1(img.tobytes()).hexdigest()

    img_file_name = f"{img_hash}.jpeg"

    output_path = os.path.join(output_dir, img_file_name)

    img.save(output_path, quality=95, optimize=True)

    return output_path, file_name