from flask import Blueprint, render_template


_home = Blueprint("home", __name__, template_folder="templates")


@_home.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


def create_blueprint() -> Blueprint:
    return _home
