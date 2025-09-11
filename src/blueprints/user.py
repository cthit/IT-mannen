
from flask import Blueprint, render_template, flash
from forms import create_post_form
from src.database.pr import create_post, set_timed_post
from src.database.connection_pr import pr_cursor

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

        # If the post is timed, set the timed post
        if form.is_timed.data:
            @pr_cursor
            def get_latest_post_id(cur):
                cur.execute("SELECT id FROM Posts WHERE owner=%s ORDER BY id DESC LIMIT 1;", ("admin",))
                row = cur.fetchone()
                return row[0] if row else None
            post_id = get_latest_post_id()
            if post_id:
                set_timed_post(
                    post_id=post_id,
                    start_time=str(form.start_time.data),
                    end_time=str(form.end_time.data)
                )
        flash("post created successfully", "success")
        return render_template("user.html", form=form)
    else:
        flash("post creation failed, form.validate_on_submit() is false", "error")
    return render_template("user.html", form=form)


def create_blueprint() -> Blueprint:
    return _user
