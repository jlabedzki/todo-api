from flask import Flask, request, Response, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user
from db.models import *

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://johnny:johnny@localhost:5432/todo-api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initilialize login manager
login = LoginManager(app)
login.init_app(app)

#


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    user_exists = db.session.query(db.exists().where(
        User.username == username)).scalar()

    if user_exists:
        return jsonify({"hello": "world"})
        return Response(409)
    else:
        # hash password before storing in db
        hashed_password = bcrypt.generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"user": "created"})


@app.route('/login', methods=['POST'])
def login():
    # if account exists and credentials validate, return 200 and the userID
    # if credentials fail validation return 401 (invalid password)
    # if account doesn't exist return 404 (we could not find an account associated with that username)
    return jsonify({"hello": "world"})


if __name__ == "__main__":
    app.run(debug=True)
