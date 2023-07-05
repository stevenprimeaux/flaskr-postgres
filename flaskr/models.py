"""Define data model."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Define users table."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def insert(self):
        """Insert user into database."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update user in database."""
        db.session.commit()

    def delete(self):
        """Delete user from database."""
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    """Define posts table."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    author = db.relationship("User", backref=db.backref("author"))

    def insert(self):
        """Insert post into database."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Update post in database."""
        db.session.commit()

    def delete(self):
        """Delete post from database."""
        db.session.delete(self)
        db.session.commit()


def get_posts_all():
    """Get all blog posts."""
    return db.session.execute(
        db.select(Post).order_by(Post.created.desc())
    ).scalars()


def get_post_by_id(post_id):
    """Get blog post by id."""
    return db.session.execute(
        db.select(Post).filter_by(id=post_id)
    ).scalar_one_or_none()


def get_users_all():
    """Get all users."""
    return db.session.execute(
        db.select(User).order_by(User.username)
    ).scalars()


def get_user_by_id(user_id):
    """Get user by id."""
    return db.session.execute(
        db.select(User).filter_by(id=user_id)
    ).scalar_one_or_none()


def get_user_by_username(username):
    """Get user by username."""
    return db.session.execute(
        db.select(User).filter_by(username=username)
    ).scalar_one_or_none()
