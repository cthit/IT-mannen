from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    g
)
from flask.typing import ResponseReturnValue

from .auth import login_required
from forms import create_post_form
from database.pr import create_post, create_timed_post

_create_post = Blueprint("create_post", __name__, template_folder="templates")
 

@_create_post.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post_page() -> ResponseReturnValue:
    form = create_post_form()
    
    user = g.get("user")
    groups = [group.get("prettyName","") for group in user.get("groups",[])]
    form.group.choices = groups

    if request.method == "GET":
        return render_template("create_post.html", form=form)

    if request.method == "POST":
        return _create_post_post(form)

    return redirect("/")


def _create_post_post(form: create_post_form) -> ResponseReturnValue:
    if not form.validate_on_submit():  # type: ignore[reportUnknownMemberType]
        return render_template("create_post.html", form=form)
    
    assert form.description.data is not None
    if form.is_timed.data:
        assert form.start_time.data is not None
        assert form.end_time.data is not None

        post_id = create_timed_post(
            description=form.description.data,
            group = str(form.group.data),
            start_time=form.start_time.data,
            end_time=form.end_time.data,
        )
    else:
        post_id = create_post(description=form.description.data,group=form.group.data)

    file_data = form.file.data
    file_data.save(f"/app/src/images/{post_id}")

    return redirect("/")


def create_blueprint() -> Blueprint:
    return _create_post
