from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    """ User model """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = self._hash_password(password)

    @staticmethod
    def _hash_password(password: str):
        return bcrypt.generate_password_hash(password).decode('utf-8')


class Todo(db.Model):
    """
    Todo model
    The priority will default to 1 (low), and can be any of (1, 2, 3 (low, medium, high))
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'))
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date(), nullable=False)
    priority = db.Column(db.Integer, default=1, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, user_id: int, title: str, date: str, priority=1, completed=False):
        self.user_id = user_id
        self.title = title
        self.date = date
        self.priority = priority
        self.completed = completed
