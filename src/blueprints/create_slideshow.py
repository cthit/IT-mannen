from flask import Blueprint, render_template, request, redirect
from flask.typing import ResponseReturnValue

from forms import create_slideshow_form
from database.pr import create_slideshow

_create_slideshow = Blueprint("create_slideshow", __name__, template_folder="templates")


@_create_slideshow.route("/create_slideshow", methods=["GET", "POST"])
def create_slideshow_view() -> ResponseReturnValue:
    form = create_slideshow_form()
    if request.method == "GET":
        return render_template("create_slideshow.html", form=form)

    if request.method == "POST":
        return _create_slideshow_post(form)
    
    return redirect("/")




def _create_slideshow_post(form : create_slideshow_form) -> ResponseReturnValue:
    if not form.validate_on_submit(): # type: ignore[reportUnknownMemberType]
        return render_template("create_slideshow.html", form=form)

    name = form.name.data
    assert name is not None

    new_id = create_slideshow(name=name)

    return redirect(f"/edit_slideshow/{new_id}")




def create_blueprint() -> Blueprint:
    return _create_slideshow
