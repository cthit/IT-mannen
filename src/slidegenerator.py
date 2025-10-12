import time

from database.pr import get_content_from_slideshow

def generate(slideshow_id : int, interval : float):

    while True:
        for post in get_content_from_slideshow(slideshow_id=slideshow_id):
            with open(f"src/images/{post.file_name}", "rb") as f:
                img_data = f.read()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/png\r\n\r\n" + img_data + b"\r\n"
            )
            time.sleep(interval)