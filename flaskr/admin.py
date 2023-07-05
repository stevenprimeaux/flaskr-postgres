"""Define admin blueprint."""

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash

from flaskr.models import get_users_all, get_user_by_id

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
def index():
    """Fetch users to display on admin page."""
    users = get_users_all()
    return render_template("admin/index.html", users=users)


@bp.route("/<int:user_id>/update", methods=["GET", "POST"])
def update(user_id):
    """Edit user."""
    user = get_user_by_id(user_id)

    if request.method == "POST":
        password = request.form["password"]
        error = None

        if not password:
            error = "Password is required."

        if error is not None:
            flash(error)
        else:
            user.password = generate_password_hash(password)
            user.update()
            return redirect(url_for("admin.index"))

    return render_template("admin/update.html", user=user)


@bp.route("/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    """Delete user."""
    user = get_user_by_id(user_id)
    user.delete()
    return redirect(url_for("admin.index"))
