from flask import Flask, Response, Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from marshmallow import Schema, fields
from src.db.models import *
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

app = Flask(__name__)
bcrypt = Bcrypt(app)

authentication = Blueprint('authentication', __name__)

class UserAuthenticationSchema(Schema):
    username: fields.String(required=True)
    password: fields.String(required=True)


@authentication.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    user_exists = db.session.query(db.exists().where(
        User.username == username)).scalar()

    if user_exists:
        return jsonify({"Message": "That user already exists"}), 409
    else:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"Message": "User created succesfully"}), 201


@authentication.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"Message": "That user doesn't exist"}), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"Message": "Incorrect password"}), 401

    access_token = create_access_token(identity=username)

    return jsonify({"username": user.username, "user_id": user.id, "access_token": access_token}), 200


@authentication.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    current_user = get_jwt_identity() 

    if current_user is None:
      return Response(status=401)

    return Response(status=200)
