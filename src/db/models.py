from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """ User model """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Todo(db.Model):
    """ Todo model """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    priority = db.Column(db.Integer, default=1, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
