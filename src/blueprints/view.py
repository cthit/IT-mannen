from flask import Response, Blueprint, request

from slidegenerator import generate

_view = Blueprint("view", __name__, template_folder="templates")


@_view.route("/tv")
def slideshow_stream():
    view_id = int(request.args.get("view_id", "0")) # TODO handle view_id is None
    interval = float(request.args.get("interval", "5"))

    return Response(generate(view_id=view_id, interval=interval), mimetype="multipart/x-mixed-replace; boundary=frame")


def create_blueprint() -> Blueprint:
    return _view

