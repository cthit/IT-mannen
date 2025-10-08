from flask import Blueprint, render_template, request, redirect
from database.pr_tuples import Post
from database.pr import get_content_from_inSlideshow,get_slideshow,add_post_to_inSlideshow, remove_post_from_inSlideshow
from forms import edit_slideshow_form

_edit_slideshow = Blueprint("edit_slideshow", __name__, template_folder="templates")


@_edit_slideshow.route("/edit_slideshow/<int:slideshow_id>", methods=["GET","POST"])
def index(slideshow_id: int) -> str:
    if request.method == "GET":
        if slideshow_id is None:
            return redirect("/")

        #fetch posts in slideshow from db
        posts: tuple[Post, ...] = get_content_from_inSlideshow(int(slideshow_id))
        form = edit_slideshow_form()
        slideshow_name = get_slideshow(slideshow_id).name
        if slideshow_name is not None:
            return render_template("edit_slideshow.html", form=form, slideshow_name=slideshow_name, posts=posts)
        else:
            return render_template("edit_slideshow.html", form=form, slideshow_name=None, posts=posts)

    pass
    # get post_ids, and add posts not in slideshow to the slideshow
    form = edit_slideshow_form()
   
    #if form.validate_on_submit():, might not be needed since a slideshow can be empty 
    current_posts = set(post.id for post in get_content_from_inSlideshow(slideshow_id))
    new_posts = set(form.post_ids)

    # Add new posts not already in slideshow
    # TODO check if post_id is valid, perhaps in a lower layer, e.g. in database/pr.py
    for post_id in new_posts - current_posts:
        add_post_to_inSlideshow(slideshow_id, post_id)

    # Remove posts that are no longer selected
    for post_id in current_posts - new_posts:
        remove_post_from_inSlideshow(slideshow_id, post_id)
    return redirect(f"/tv/{slideshow_id}")


def create_blueprint() -> Blueprint:
    return _edit_slideshow
