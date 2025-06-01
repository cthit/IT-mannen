from flask import Blueprint, render_template
from forms import create_post_form


_user = Blueprint("user", __name__, template_folder="templates")


@_user.route("/user", methods=["GET", "POST"])
def fridge_page() -> str:
    form = create_post_form()
    return render_template("user.html", form=form)


def create_blueprint() -> Blueprint:
    return _user
