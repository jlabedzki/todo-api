from flask import Flask, Response, Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended.utils import create_refresh_token, unset_jwt_cookies
from src.db.models import *
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)

app = Flask(__name__)
bcrypt = Bcrypt(app)

authentication = Blueprint("authentication", __name__)


@authentication.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    user_exists = db.session.query(
        db.exists().where(User.username == username)
    ).scalar()

    if user_exists:
        return jsonify({"Message": "That user already exists"}), 409

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return (
        jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        201,
    )


@authentication.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"Message": "That user doesn't exist"}), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"Message": "Incorrect password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return (
        jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        ),
        200,
    )


@authentication.route("/user", methods=["GET"])
@jwt_required()
def get_user_with_jwt():
    current_user = get_jwt_identity()

    user = User.query.filter_by(username=current_user).first()

    if user is None:
        return Response(status=401)

    return jsonify({"user_id": user.id, "username": user.username}), 200


@authentication.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@authentication.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    response = jsonify({"Message": "Logout successful"})
    unset_jwt_cookies(response)
    return response
