from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """ User model """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Status(db.Model):
    """ Status model """

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(25), unique=True, nullable=False)


class Todo(db.Model):
    """ Todo model """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Date(), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'status.id'), default=1)
