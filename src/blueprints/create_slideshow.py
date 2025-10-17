from flask import Blueprint, render_template, request, flash, redirect
from forms import create_slideshow_form
from database.pr import create_slideshow
from .auth import login_required

_create_slideshow = Blueprint("create_slideshow", __name__, template_folder="templates")


@_create_slideshow.route("/create_slideshow", methods=["GET", "POST"])
@login_required
def create_slideshow_view() -> str:
    if request.method == "GET":
        form = create_slideshow_form()
        return render_template("create_slideshow.html", form=form)

    form = create_slideshow_form()
    if form.validate_on_submit():
        # Process the form data
        filedata = form.name.data
        new_id = create_slideshow(
            name=filedata
            )
        flash("Slideshow created successfully!", "success")
        return redirect(f"/edit_slideshow/{new_id}")
    else:
        flash("Error in form submission. Please check your inputs.", "error")
        return render_template("create_slideshow.html", form=form)


def create_blueprint() -> Blueprint:
    return _create_slideshow
