from flask import Blueprint, render_template, request, redirect, g
from flask.typing import ResponseReturnValue

from src.forms import create_slideshow_form
from src.database.pr import create_slideshow
from .auth import login_required

_create_slideshow = Blueprint("create_slideshow", __name__, template_folder="templates")


@_create_slideshow.route("/create_slideshow", methods=["GET", "POST"])
@login_required
def create_slideshow_view() -> ResponseReturnValue:
    form = create_slideshow_form()

    # get all possible owners (user and groups) for the select field
    user = g.get("user")["nick"]
    groups = [group.get("prettyName") for group in g.get("user")["groups"]]
    owners = [user] + groups
    form.owner.choices = owners

    #visibility options are set in the form definition since they are static

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

    owner_name = form.owner.data
    owner = None
    if owner_name == g.get("user")["nick"]:
        owner = g.get("user")["actor_id"]
    else:
        for group in g.get("user")["groups"]:
            if group.get("prettyName") == owner_name:
                owner = group.get("actor_id")
                break
        
    visibility = form.visibility.data

    new_id = create_slideshow(name=name, owner = owner, visibility=visibility)

    return redirect(f"/edit_slideshow/{new_id}")




def create_blueprint() -> Blueprint:
    return _create_slideshow
