import time

from database.pr import get_content_from_postview

def generate(view_id : int, interval : float):

    while True:
        for post in get_content_from_postview(view_id=view_id):
            with open(f"src/images/{post.file_name}", "rb") as f:
                img_data = f.read()
            yield (
                b"--frame\r\n"
                b"Content-Type: image/png\r\n\r\n" + img_data + b"\r\n"
            )
            time.sleep(interval)