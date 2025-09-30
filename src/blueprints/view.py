import time
from flask import Flask, Response, Blueprint

_view = Blueprint("view", __name__, template_folder="templates")


@app.route("/slideshow_stream")
def slideshow_stream():
    def generate():
        slides = ["static/slide1.png", "static/slide2.png", "static/slide3.png"]
        while True:
            for slide in slides:
                with open(slide, "rb") as f:
                    img_data = f.read()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/png\r\n\r\n" + img_data + b"\r\n"
                )
                time.sleep(5)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")




