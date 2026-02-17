from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    g,
    jsonify  # Import jsonify for returning JSON responses
)
from flask.typing import ResponseReturnValue

from .auth import login_required
from src.forms import create_post_form
from src.database.pr import create_post, create_timed_post

_create_post = Blueprint("create_post", __name__, template_folder="templates")

@_create_post.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post_page() -> ResponseReturnValue:
    form = create_post_form()


    if request.method == "GET":
        user = g.get("user")["nick"]
        groups = [group.get("prettyName") for group in g.get("user")["groups"]]
        owners = [user] + groups
        form.owner.choices = owners
        return render_template("create_post.html", form=form)

    if request.method == "POST":
        return _create_post_post(form)

    return redirect("/")


def _create_post_post(form: create_post_form) -> ResponseReturnValue:
    if not form.validate_on_submit():  # type: ignore[reportUnknownMemberType]
        return render_template("create_post.html", form=form)

    if form.description.data is None:
        return render_template("create_post.html", form=form, error="Description is required"), 400
    if form.is_timed.data:
        assert form.start_time.data is not None
        assert form.end_time.data is not None

        owner_name = form.owner.data
        owner = None
        if owner_name == g.get("user")["nick"]:
            owner = g.get("user")["actor_id"]
        else:
            for group in g.get("user")["groups"]:
                if group.get("prettyName") == owner_name:
                    owner = group.get("actor_id")
                    break
        

        post_id = create_timed_post(
            name = form.name.data,
            description=form.description.data,
            owner = owner, 
            start_time=form.start_time.data,
            end_time=form.end_time.data,
        )
    else:
        post_id = create_post(
            name = form.name.data,
            description=form.description.data,
            owner = owner, 
        )

    file_data = form.file.data
    file_data.save(f"/app/src/images/{post_id}.png")

    return redirect("/")


def create_blueprint() -> Blueprint:from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    g,
    jsonify  # Import jsonify for returning JSON responses
)
from flask.typing import ResponseReturnValue

from .auth import login_required
from src.forms import create_post_form
from src.database.pr import create_post, create_timed_post

_create_post = Blueprint("create_post", __name__, template_folder="templates")

@_create_post.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post_page() -> ResponseReturnValue:
    form = create_post_form()

    # get all possible owners (user and groups) for the select field
    user = g.get("user")["nick"]
    groups = [group.get("prettyName") for group in g.get("user")["groups"]]
    owners = [user] + groups
    form.owner.choices = owners

    if request.method == "GET":
        
        return render_template("create_post.html", form=form)

    if request.method == "POST":
        return _create_post_post(form)

    return redirect("/")


def _create_post_post(form: create_post_form) -> ResponseReturnValue:
    if not form.validate_on_submit():  # type: ignore[reportUnknownMemberType]
        return render_template("create_post.html", form=form)

    if form.description.data is None:
        return render_template("create_post.html", form=form, error="Description is required"), 400
        
    owner_name = form.owner.data
    owner = None
    if owner_name == g.get("user")["nick"]:
        owner = g.get("user")["actor_id"]
    else:
        for group in g.get("user")["groups"]:
            if group.get("prettyName") == owner_name:
                owner = group.get("actor_id")
                break
        
    
    if form.is_timed.data:
        assert form.start_time.data is not None
        assert form.end_time.data is not None

    

        post_id = create_timed_post(
            name = form.name.data,
            description=form.description.data,
            owner = owner, 
            start_time=form.start_time.data,
            end_time=form.end_time.data,
        )
    else:
        post_id = create_post(
            name = form.name.data,
            description=form.description.data,
            owner = owner, 
        )

    file_data = form.file.data
    file_data.save(f"/app/src/images/{post_id}.png")

    return redirect("/")


def create_blueprint() -> Blueprint:
    return _create_post

    return _create_post
