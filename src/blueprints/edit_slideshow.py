from flask import Blueprint, render_template, request, redirect, flash, g
from src.database.pr_tuples import Post, Slideshow
from src.database.pr import get_content_from_SlideshowContents,get_slideshow,add_post_to_SlideshowContents, remove_post_from_SlideshowContents, get_all_owned_non_expired_posts, get_slideshow_owner
from src.forms import edit_slideshow_form
from .auth import login_required

_edit_slideshow = Blueprint("edit_slideshow", __name__, template_folder="templates")


@_edit_slideshow.route("/edit_slideshow/<int:slideshow_id>", methods=["GET", "POST"])
@login_required
def index(slideshow_id: int):
    #create forms
    owner = False
     # Start with the actor_id from user
    actor_id = g.get("user")["actor_id"]
    groups = g.get("user")["groups"]

    actor_ids = [actor_id]  # Start with the actor_id from user

    for group in groups:
        actor_ids.append(group.get("actor_id")) 
        
    for actor_id in actor_ids:
        if actor_id == get_slideshow_owner(slideshow_id):
            owner = True
            break

    if not owner:
        flash("You do not have permission to edit this slideshow.")
        return redirect("/")


    add_form = edit_slideshow_form()
    remove_form = edit_slideshow_form()

    slideshow = get_slideshow(slideshow_id)
    slideshow_name = slideshow.name

    nonExpired_posts = get_all_owned_non_expired_posts(actor_ids=actor_ids)
    current_posts = get_content_from_SlideshowContents(slideshow_id)
    current_posts_ids = [post.id for post in current_posts]

    # Update choices for the SelectMultipleField to exclude already added posts
    newchoices = [(post.id, post.description) for post in nonExpired_a = [posts if post.id not in current_posts_ids]
    add_form.post_ids.choices = newchoices

    # Choices for removing posts are the currently added posts
    remove_form.post_ids.choices = [(post.id, post.description) for post in current_posts]

    if add_form.validate_on_submit():
    
        new_posts = add_form.post_ids.data
    
        # Add and remove posts accordingly
        for post_id in new_posts:
            if post_id not in current_posts_ids:
                add_post_to_SlideshowContents(slideshow_id, post_id)
        
        return redirect(request.url)

    if remove_form.validate_on_submit():
        removed_posts = remove_form.post_ids.data

        for post_id in removed_posts:
            if post_id in current_posts_ids:
                remove_post_from_SlideshowContents(slideshow_id, post_id)
        return redirect(request.url)


    return render_template(
        "edit_slideshow.html",
        add_form=add_form,
        remove_form=remove_form,
        slideshow_name=slideshow_name,
        slideshow_id=slideshow_id,
        current_posts=current_posts,
    )



def create_blueprint() -> Blueprint:
    return _edit_slideshow
