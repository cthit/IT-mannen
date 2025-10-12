from flask import Blueprint, render_template, request

from database.pr import get_slideshows


_home = Blueprint("home", __name__, template_folder="templates")


@_home.route("/", methods=["GET"])
def index() -> str:
    slideshow_id = request.args.get("slideshow_id")
    interval = float(request.args.get("interval", "5"))

    if slideshow_id is not None:
        return render_template("tv.html", slideshow_id=int(slideshow_id), interval=interval)

    return render_template("home.html", slideshows=get_slideshows())


def create_blueprint() -> Blueprint:
    return _home
