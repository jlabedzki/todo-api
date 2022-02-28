from flask import Flask
from models import *
from decouple import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def main():
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
