
from flask import Blueprint, render_template, flash
from forms import create_post_form
from database.pr import create_post, set_timed_post

_user = Blueprint("user", __name__, template_folder="templates")


@_user.route("/user", methods=["GET", "POST"])
def user_page() -> str:
    form = create_post_form()
    if form.validate_on_submit():
        file_data = form.file.data
        filename = None
        if file_data:
            filename = file_data.filename
            file_data.save(f"static/uploads/{filename}")
        else:
            flash("No file uploaded", "info")

        # Use psycopg2-based function to create post
        create_post(
            description=form.description.data,
            file_name=filename
        )
        flash("post created successfully", "success")
        if form.is_timed.data:
            set_timed_post(form.description.data)
            flash("post set as timed", "info")
        else:
            flash("post is not timed", "info")
        return render_template("user.html", form=form)
    else:
        flash("post creation failed, form.validate_on_submit() is false", "error")
    return render_template("user.html", form=form)


def create_blueprint() -> Blueprint:
    return _user
