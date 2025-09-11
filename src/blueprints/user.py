
from flask import Blueprint, render_template, flash, request
from forms import create_post_form
from database.pr import create_post, create_timed_post

_user = Blueprint("user", __name__, template_folder="templates")


@_user.route("/user", methods=["GET", "POST"])
def user_page() -> str:
    if request.method == "GET":
        form = create_post_form()
        return render_template("user.html", form=form)
    form = create_post_form()
    if form.validate_on_submit():
        file_data = form.file.data
        filename = None
        if file_data:
            filename = file_data.filename
            file_data.save(f"static/uploads/{filename}")
            flash("File uploaded successfully", "success")
        else:
            flash("No file uploaded", "info")

        # Use psycopg2-based function to create post
        if form.is_timed.data:
            create_timed_post(
                description=form.description.data,
                file_name=filename,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                )
            flash("post set as timed", "info")
        else:
            create_post(
            description=form.description.data,
            file_name=filename
            )
            flash("post is not timed", "info")
        
        flash("post created successfully", "success")
        return redirect("/")
    else:
        flash("post creation failed, form.validate_on_submit() is false", "error")
    return redirect("/")


def create_blueprint() -> Blueprint:
    return _user
