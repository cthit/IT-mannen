from flask import Blueprint, render_template, request, redirect
from database.pr_tuples import Post, Slideshow
from database.pr import get_content_from_inSlideshow,get_slideshow,add_post_to_inSlideshow, remove_post_from_inSlideshow, get_all_nonExpired_post
from forms import edit_slideshow_form


_edit_slideshow = Blueprint("edit_slideshow", __name__, template_folder="templates")


@_edit_slideshow.route("/edit_slideshow/<int:slideshow_id>", methods=["GET","POST"])
def index(slideshow_id: int) -> str:
    if request.method == "GET":
        if slideshow_id is None:
            return redirect("/")

        #fetch posts in slideshow from db
        current_posts: tuple[Post, ...] = get_content_from_inSlideshow(int(slideshow_id))
        form = edit_slideshow_form()
        slideshow :Slideshow = get_slideshow(slideshow_id)
        slideshow_name = slideshow.name
        nonExpired_posts = get_all_nonExpired_post()
        if slideshow_name is not None:
            return render_template("edit_slideshow.html", form=form, slideshow_name=slideshow_name, posts=current_posts, nonExpired_posts=nonExpired_posts)
        else:
            return render_template("edit_slideshow.html", form=form, slideshow_name=None, posts=current_posts, nonExpired_posts=nonExpired_posts)

    # get post_ids, and add posts not in slideshow to the slideshow
    form = edit_slideshow_form()
   
    #if form.validate_on_submit():, might not be needed since a slideshow can be empty 
    current_posts: tuple[Post, ...] = get_content_from_inSlideshow(int(slideshow_id))
    current_posts_set = set(post.id for post in current_posts)  # Extract IDs for easier comparison
    new_posts_set = set(form.post_ids.data)  # Convert to set for easier comparison


    # Add new posts not already in slideshow
    # TODO check if post_id is valid, perhaps in a lower layer, e.g. in database/pr.py
    for post_id in new_posts_set - current_posts:
        add_post_to_inSlideshow(slideshow_id, post_id)

    # Remove posts that are no longer selected
    for post_id in current_posts - new_posts_set:
        remove_post_from_inSlideshow(slideshow_id, post_id)

    slideshow :Slideshow = get_slideshow(slideshow_id)
    slideshow_name = slideshow.name
    current_posts = get_content_from_inSlideshow(int(slideshow_id))
    nonExpired_posts = get_all_nonExpired_post()
    return render_template("edit_slideshow.html", form=form, slideshow_name=slideshow_name, posts=current_posts, nonExpired_posts=nonExpired_posts)


def create_blueprint() -> Blueprint:
    return _edit_slideshow
