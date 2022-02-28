from flask import Flask, Blueprint, Response, jsonify, request
from flask_login import login_user, logout_user
from flask_bcrypt import Bcrypt
from db.models import *

app = Flask(__name__)
bcrypt = Bcrypt(app)

authentication = Blueprint('authentication', __name__)


@authentication.route('/register', methods=['POST'])
def register():
    request.get_json(force=True)
    username = request.json['username']
    password = request.json['password']

    user_exists = db.session.query(db.exists().where(
        User.username == username)).scalar()

    if user_exists:
        return Response(status=409)
    else:
        # hash password before storing in db
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return Response(status=201)


@authentication.route('/login', methods=['POST'])
def login():
    request.get_json(force=True)
    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user:
        # Compare the password input to the hashed password in the db
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'user_id': user.id})
        else:
            return Response(status=401)
    else:
        return Response(status=404)


@authentication.route('/logout', methods=['GET'])
def logout():

    logout_user()
    return Response(status=200)
