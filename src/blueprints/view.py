from flask import Response, Blueprint, request

from slidegenerator import generate

_view = Blueprint("view", __name__, template_folder="templates")


@_view.route("/tv/<int:slideshow_id>")
def slideshow_stream(slideshow_id:  int):
    # TODO handle id = 0
    interval = float(request.args.get("interval", "5"))

    return Response(generate(slideshow_id=slideshow_id, interval=interval), mimetype="multipart/x-mixed-replace; boundary=frame")


def create_blueprint() -> Blueprint:
    return _view

