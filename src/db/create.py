from flask import Flask
from models import *
from decouple import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

statuses = ['active', 'cancelled', 'complete']


def main():
    db.create_all()
    for status in statuses:
        new_status = Status(status=status)
        db.session.add(new_status)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
