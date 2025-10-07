from flask import Blueprint, render_template, request

from database.pr import get_slideshows


_home = Blueprint("home", __name__, template_folder="templates")


@_home.route("/", methods=["GET"])
def index() -> str:
    view_id = request.args.get("view_id")
    interval = float(request.args.get("interval", "5"))

    if view_id is not None:
        return render_template("tv.html", view_id=int(view_id), interval=interval)

    return render_template("home.html", routes=get_slideshows())


def create_blueprint() -> Blueprint:
    return _home
