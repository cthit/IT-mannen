from flask import Blueprint, render_template, request

from database.pr import get_postviews


_home = Blueprint("home", __name__, template_folder="templates")


@_home.route("/", methods=["GET"])
def index() -> str:
    view_id = request.args.get("id")

    if view_id is not None:
        return render_template("tv.html", view_id=view_id)

    return render_template("home.html", routes=get_postviews(), view_id=view_id)


def create_blueprint() -> Blueprint:
    return _home
