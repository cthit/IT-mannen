
from flask import Blueprint, render_template, flash, request, redirect, current_app as app
from forms import create_post_form
from database.pr import create_post, create_timed_post

_user = Blueprint("user", __name__, template_folder="templates")


@_user.route("/user", methods=["GET", "POST"])
def user_page() -> str:
    if request.method == "GET":
        form = create_post_form()
        return render_template("user.html", form=form)
    
    form = create_post_form()
    if not form.validate_on_submit():
        return redirect("/error")
    file_data = form.file.data
    # Save uploaded file to a new file in the volume if present
    
    if file_data:
        filename = file_data.filename
        file_data.save(f"/app/src/images/{filename}")
        if file_data:
            app.logger.info("File uploaded successfully")
        else:
            app.logger.info("No file uploaded")
    # Use psycopg2-based function to create post
    if form.is_timed.data:
        create_timed_post(
            description=form.description.data,
            file_name=filename,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
        )
    else:
        create_post(
            description=form.description.data,
            file_name=filename
        )
    
    return redirect("/")
   # else:
   #     flash("post creation failed, form.validate_on_submit() is false", "error")
   #     #print(form.validate_on_submit())
    #return redirect("/")


def create_blueprint() -> Blueprint:
    return _user
