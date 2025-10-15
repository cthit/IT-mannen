from flask import (
    Blueprint,
    render_template,
    flash,
    request,
    redirect,
    current_app as app,
    Response,
)
from flask.typing import ResponseReturnValue
from forms import create_post_form
from database.pr import create_post, create_timed_post
from typing import cast

_user = Blueprint("user", __name__, template_folder="templates")


@_user.route("/user", methods=["GET", "POST"])
def user_page() -> ResponseReturnValue:
    form = create_post_form()

    if request.method == "GET":
        return render_template("user.html", form=form)

    if request.method == "POST":
        return _user_page_post(form)

    return redirect("/")


def _user_page_post(form: create_post_form) -> ResponseReturnValue:
    if not form.validate_on_submit():  # type: ignore[reportUnknownMemberType]
        return render_template("user.html", form=form)

    if form.is_timed.data:
        post_id = create_timed_post(
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
        )
    else:
        post_id = create_post(description=form.description.data)

    file_data = form.file.data

    file_data.save(f"/app/src/images/{post_id}")
    if file_data:
        app.logger.info("File uploaded successfully")
    else:
        app.logger.info("No file uploaded")

    return redirect("/")

    ## TODO check that file has .png extension, file is actually a png and the file is not None


def create_blueprint() -> Blueprint:
    return _user
