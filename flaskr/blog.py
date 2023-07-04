"""Define blog blueprint."""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.models import get_posts_all, get_post_by_id, Post

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Fetch blog posts to display on home page."""
    posts = get_posts_all()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create blog post."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."
        elif not body:
            error = "Body is required."

        if error is not None:
            flash(error)
        else:
            post = Post()
            post.title = title
            post.body = body
            post.author_id = g.user.id
            post.insert()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update(post_id):
    """Update blog post."""
    post = get_post(post_id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."
        elif not body:
            error = "Body is required."

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            post.update()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id):
    """Delete blog post."""
    post = get_post(post_id)
    post.delete()
    return redirect(url_for("blog.index"))


def get_post(post_id, check_author=True):
    """Fetch blog post."""
    post = get_post_by_id(post_id)

    if post is None:
        abort(404, f"Post id {post_id} doesn't exit.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post
