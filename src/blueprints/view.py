from flask import Response, Blueprint, request

from slidegenerator import generate

_view = Blueprint("view", __name__, template_folder="templates")


@_view.route("/tv")
def slideshow_stream():
    slideshow_id = int(request.args.get("slideshow_id", "0")) # TODO handle view_id is None
    interval = float(request.args.get("interval", "5"))

    return Response(generate(slideshow_id=slideshow_id, interval=interval), mimetype="multipart/x-mixed-replace; boundary=frame")


def create_blueprint() -> Blueprint:
    return _view

